"""Local demo web chat for the Northbound RAG assistant.

A thin wrapper: it calls the existing answer() from src/generate.py and changes
nothing in the RAG core or the eval. The API key is loaded server-side by
load_dotenv() (via generate.py) and never reaches the browser.

Pages: /  customer chat  ·  /monitor  answer-quality dashboard (reads eval/monitor_*.json)

Run:  .venv/bin/python webapp/app.py          -> http://localhost:5000
      PORT=5001 .venv/bin/python webapp/app.py   (if macOS AirPlay holds port 5000)
"""
import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from generate import answer  # noqa: E402  (also runs load_dotenv())
from index import embed, get_collection  # noqa: E402
from ingest import load_docs  # noqa: E402
import monitor as monitor_run  # noqa: E402  (the same src/monitor.py the CLI runs)

TITLES = {c.doc_id: c.title for c in load_docs()}   # doc id -> title, from the KB loader
MAX_QUESTION = 500

app = Flask(__name__)
col = get_collection()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/ask")
def ask():
    question = str((request.get_json(silent=True) or {}).get("question", "")).strip()
    if not question:
        return jsonify(error="Please type a question."), 400
    if len(question) > MAX_QUESTION:
        return jsonify(error=f"Please keep questions under {MAX_QUESTION} characters."), 400
    try:
        r = answer(question, col=col)
    except Exception as e:  # API down, bad key, network: show a friendly error, log the detail
        app.logger.exception("answer() failed")
        return jsonify(error="The assistant is unavailable right now. Please try again.",
                       detail=type(e).__name__), 502
    sources = [] if r["refused"] else [
        {"id": d, "title": TITLES[d]} for d in r["cited_ids"] if d in TITLES
    ]
    return jsonify(answer=r["answer"], sources=sources, refused=r["refused"])


# --- /monitor: the "Answer quality" dashboard (DL16). Reads the monitor's JSON only. ---
EVAL_DIR = Path(__file__).resolve().parent.parent / "eval"
SCALE_LO = 85.0   # gauge scale 85–100%, as in the design


def _chart(runs: list[dict], target: dict) -> dict:
    """SVG geometry for the grounding-score-by-run line chart (real runs only)."""
    scores = [r["grounding_score"] for r in runs if r.get("grounding_score") is not None]
    lo = float(min([88, *[int((s - 2) // 4 * 4) for s in scores]]))   # gridlines every 4 pts, as designed
    y = lambda v: round(220 - (v - lo) / (100 - lo) * 200, 1)
    n = len(runs)
    x = (lambda i: 378.0) if n == 1 else (lambda i: round(60 + i * 632 / (n - 1), 1))
    points, notes = [], []
    for i, r in enumerate(runs):
        s = r.get("grounding_score")
        if s is None:
            continue
        points.append({"x": x(i), "y": y(s), "score": s, "run": r["run"],
                       "below": s < target["band_low"]})
        changes = []
        if i and r.get("kb_docs") != runs[i - 1].get("kb_docs"):
            changes.append(f"KB {runs[i - 1].get('kb_docs')} → {r.get('kb_docs')} docs")
        if i and r.get("judge_version") != runs[i - 1].get("judge_version"):
            old, new = (str(v).split()[-1] for v in (runs[i - 1].get("judge_version"), r.get("judge_version")))
            changes.append(f"Judge {old} → {new}")
        if changes:
            near_right = x(i) > 520                      # keep the label inside the chart
            notes.append({"x": x(i), "text": " · ".join(changes),
                          "tx": x(i) - 6 if near_right else x(i) + 6, "anchor": "end" if near_right else "start"})
    ticks = list(range(100, int(lo) - 1, -4))
    return {
        "points": points, "notes": notes, "polyline": " ".join(f"{p['x']},{p['y']}" for p in points),
        "grid": [{"y": y(t), "label": f"{t:g}%"} for t in ticks],
        "band_y": y(target["band_high"]), "band_h": round(y(target["band_low"]) - y(target["band_high"]), 1),
        "target_y": y(target["target"]),
        "xlabels": [{"x": p["x"], "run": p["run"]} for i, p in enumerate(points)
                    if n <= 8 or i % max(1, n // 7) == 0 or i == len(points) - 1],
    }


def _pct(v: float) -> float:
    return round((min(max(v, SCALE_LO), 100) - SCALE_LO) / (100 - SCALE_LO) * 100, 2)


@app.get("/monitor")
def monitor():
    try:
        latest = json.loads((EVAL_DIR / "monitor_latest.json").read_text(encoding="utf-8"))
        runs = json.loads((EVAL_DIR / "monitor_runs.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return render_template("monitor.html", empty=True)
    s, t = latest["summary"], latest["target"]
    g = s["grounding_score"]
    prev = runs[-2]["grounding_score"] if len(runs) > 1 else None
    status = ("below" if g < t["band_low"] else "above" if g > t["band_high"] else "within")
    gauge = {"score": _pct(g), "target": _pct(t["target"]), "band_left": _pct(t["band_low"]),
             "band_width": round(_pct(t["band_high"]) - _pct(t["band_low"]), 2),
             "ticks": [{"v": v, "left": _pct(v)} for v in (85, 90, 95, 100)]}
    return render_template(
        "monitor.html", empty=False, s=s, t=t, status=status, gauge=gauge, rows=latest["rows"],
        delta=None if prev is None else round(g - prev, 1), prev_run=runs[-2]["run"] if prev is not None else None,
        chart=_chart(runs, t), n_runs=len(runs),
        run_time=datetime.fromisoformat(s["timestamp"]).strftime("%-d %b %Y, %H:%M"),
        n_flagged=sum(r["flagged"] for r in latest["rows"]),
    )


# --- "Run monitor" button: one background run at a time, polled by the page for progress ---
_job = {"state": "idle"}
_job_lock = threading.Lock()


def _run_job():
    def progress(step, total, label):
        _job.update(step=step, total=total, label=label)
    try:
        summary = monitor_run.main(progress=progress, col=col)
        _job.update(state="done", run=summary["run"], score=summary["grounding_score"],
                    finished=time.time())
    except Exception as e:  # API down, bad key: report it to the page, log the detail
        app.logger.exception("monitor run failed")
        _job.update(state="error", error=f"{type(e).__name__}: the run stopped and nothing was saved.",
                    finished=time.time())


def _job_status():
    j = dict(_job)
    if j["state"] == "running":
        j["elapsed"] = round(time.time() - j["started"], 1)
    return j


@app.post("/monitor/run")
def monitor_start():
    with _job_lock:
        if _job["state"] == "running":
            return jsonify(_job_status()), 409
        _job.clear()
        _job.update(state="running", step=0, total=1, label="Starting…", started=time.time())
        threading.Thread(target=_run_job, daemon=True).start()
    return jsonify(_job_status()), 202


@app.get("/monitor/run")
def monitor_status():
    return jsonify(_job_status())


if __name__ == "__main__":
    embed(["warm up"])  # load the embedding model now, not on the first question
    port = int(os.environ.get("PORT", 5000))
    try:
        app.run(host="127.0.0.1", port=port)
    except OSError:
        sys.exit(f"Port {port} is in use (on macOS, AirPlay Receiver uses 5000). "
                 f"Try: PORT=5001 .venv/bin/python webapp/app.py")
