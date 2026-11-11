// "Run monitor" button: starts a run on the server, freezes the page behind an
// overlay and shows progress (ring + percentage + one bar per question) until
// the run is saved, then reloads the page to show the new run.
(() => {
  const overlay = document.getElementById('run-overlay');
  if (!overlay) return;
  const ring = overlay.querySelector('.ring');
  const fill = document.getElementById('ring-fill');
  const pctEl = document.getElementById('ring-pct');
  const subEl = document.getElementById('ring-sub');
  const labelEl = document.getElementById('run-label');
  const titleEl = document.getElementById('run-title');
  const timeEl = document.getElementById('run-time');
  const stepsEl = document.getElementById('run-steps');
  const actions = document.getElementById('run-actions');
  const page = [document.querySelector('header'), document.querySelector('main')];
  const CIRC = 2 * Math.PI * 68;
  const QUESTIONS = 10;

  let shown = 0;          // percentage currently drawn
  let target = 0;         // percentage the server has confirmed
  let ceiling = 0;        // how far the ring may creep before the next confirmed step
  let startedAt = Date.now();
  let timer = null, raf = null, finished = false;

  for (let i = 0; i < QUESTIONS; i++) stepsEl.appendChild(document.createElement('li'));

  const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

  function draw() {
    // ease toward the confirmed value; creep slowly within the current step so it never looks stuck
    if (shown < target) shown += Math.max(0.15, (target - shown) * 0.12);
    else if (!finished && shown < ceiling) shown += 0.02;
    shown = Math.min(shown, finished ? 100 : ceiling);
    fill.style.strokeDashoffset = CIRC * (1 - shown / 100);
    pctEl.textContent = `${Math.floor(shown)}%`;
    ring.setAttribute('aria-valuenow', String(Math.floor(shown)));
    if (!finished) timeEl.textContent = timeText();
    raf = requestAnimationFrame(draw);
  }

  let lastStep = 0, total = 21;
  function timeText() {
    const elapsed = (Date.now() - startedAt) / 1000;
    let text = `${fmt(elapsed)} elapsed`;
    if (lastStep >= 3) text += ` · about ${fmt(Math.max(0, elapsed / lastStep * (total - lastStep)))} left`;
    return text;
  }

  function freeze(on) {
    overlay.hidden = !on;
    page.forEach(el => el && (on ? el.setAttribute('inert', '') : el.removeAttribute('inert')));
    document.body.style.overflow = on ? 'hidden' : '';
  }

  function render(j) {
    total = j.total || total;
    lastStep = j.step || 0;
    if (j.started) startedAt = j.started * 1000;
    target = Math.min(100, 100 * lastStep / total);
    ceiling = Math.min(99, 100 * (lastStep + 0.9) / total);
    labelEl.textContent = j.label || '';
    const done = Math.floor(lastStep / 2);
    [...stepsEl.children].forEach((li, i) => {
      li.className = i < done ? 'full' : (i === done && lastStep % 2 === 1 ? 'half now' : (i === done ? 'now' : ''));
    });
    subEl.textContent = done < QUESTIONS ? `question ${Math.min(done + 1, QUESTIONS)} of ${QUESTIONS}` : 'saving';
  }

  function finish(j) {
    finished = true;
    clearInterval(timer);
    ring.classList.remove('running');
    if (j.state === 'done') {
      target = shown = 100;
      ring.classList.add('done');
      [...stepsEl.children].forEach(li => (li.className = 'full'));
      titleEl.textContent = `Run ${j.run} saved`;
      subEl.textContent = 'complete';
      labelEl.textContent = `Grounding score ${j.score}%. Loading the new results…`;
      timeEl.textContent = `Finished in ${fmt((j.finished * 1000 - startedAt) / 1000)}`;
      setTimeout(() => location.reload(), 1400);
    } else {
      ring.classList.add('error');
      titleEl.textContent = 'The run failed';
      subEl.textContent = 'stopped';
      labelEl.textContent = j.error || 'Something went wrong. Nothing was saved.';
      actions.hidden = false;
      document.getElementById('run-close').focus();
    }
  }

  async function poll() {
    try {
      const j = await (await fetch('/monitor/run', { cache: 'no-store' })).json();
      if (j.state === 'running') render(j);
      else if (j.state === 'done' || j.state === 'error') finish(j);
    } catch { /* server busy or restarting: keep polling */ }
  }

  function open(j) {
    finished = false; shown = 0;
    ring.className = 'ring running';
    titleEl.textContent = 'Running the monitor';
    actions.hidden = true;
    freeze(true);
    render(j);
    cancelAnimationFrame(raf); raf = requestAnimationFrame(draw);
    clearInterval(timer); timer = setInterval(poll, 700);
  }

  document.querySelectorAll('[data-run]').forEach(btn => btn.addEventListener('click', async () => {
    btn.disabled = true;
    try {
      const res = await fetch('/monitor/run', { method: 'POST' });
      open(await res.json());     // 202 started, or 409 already running: follow that run
    } catch {
      alert('Could not reach the server. Is webapp/app.py running?');
    } finally {
      btn.disabled = false;
    }
  }));

  document.getElementById('run-close').addEventListener('click', () => {
    cancelAnimationFrame(raf);
    freeze(false);
  });

  // reloaded the page mid-run? pick the running job back up
  fetch('/monitor/run', { cache: 'no-store' }).then(r => r.json())
    .then(j => { if (j.state === 'running') open(j); }).catch(() => {});
})();
