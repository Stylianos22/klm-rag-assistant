// Northbound chat: POST /ask, render the answer, its source chips, or the refusal card.
const log = document.getElementById('log');
const form = document.getElementById('ask');
const input = document.getElementById('q');
const send = form.querySelector('.send');

const DOC_ICON = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8l-5-5z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg>';
const INFO_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 7.5v.01"/></svg>';
const ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

const now = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
const esc = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Small, safe markdown subset: paragraphs, - / 1. lists, **bold**. Citation markers like [26]
// are removed from the text because the sources are shown as chips underneath.
function renderAnswer(text) {
  const clean = esc(text.replace(/\s*\[\d{1,3}(?:\s*,\s*\d{1,3})*\]/g, ''));
  const inline = s => s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  return clean.split(/\n\s*\n/).map(block => {
    const lines = block.split('\n').map(l => l.trim()).filter(Boolean);
    if (lines.length && lines.every(l => /^[-*•]\s+/.test(l)))
      return '<ul>' + lines.map(l => `<li>${inline(l.replace(/^[-*•]\s+/, ''))}</li>`).join('') + '</ul>';
    if (lines.length && lines.every(l => /^\d+[.)]\s+/.test(l)))
      return '<ol>' + lines.map(l => `<li>${inline(l.replace(/^\d+[.)]\s+/, ''))}</li>`).join('') + '</ol>';
    return `<p>${inline(lines.join('<br>'))}</p>`;
  }).join('');
}

function add(tplId) {
  const node = document.getElementById(tplId).content.firstElementChild.cloneNode(true);
  log.appendChild(node);
  log.scrollTop = log.scrollHeight;
  return node;
}

function addUser(text) {
  const n = add('tpl-user');
  n.querySelector('.bubble').textContent = text;
  n.querySelector('.meta').textContent = `You · ${now()}`;
}

function addBot({ answer, sources = [], refused = false, error = null }) {
  const n = add('tpl-bot');
  const card = n.querySelector('.card');
  const meta = n.querySelector('.meta');
  if (refused || error) {
    card.classList.add('refusal');
    const title = error ? 'Something went wrong.' : 'I don’t have that information.';
    const body = error
      ? esc(error)
      : 'This isn’t covered in Northbound’s store policies, so I can’t confirm it either way. Our customer team can give you a definite answer.';
    card.innerHTML = `${INFO_ICON}<div class="body"><p class="title">${title}</p><p class="muted">${body}</p>` +
      `<div><a class="btn-ghost" href="mailto:support@northbound.example">Contact customer service${ARROW}</a></div></div>`;
    meta.textContent = error ? `Northbound Assistant · ${now()}` : `No sources — not in the store policies · ${now()}`;
  } else {
    card.innerHTML = renderAnswer(answer);
    if (sources.length) {
      const row = document.createElement('div');
      row.className = 'sources';
      row.innerHTML = '<span class="sources-label">Sources</span>' +
        sources.map(s => `<span class="chip" title="Policy doc ${esc(s.id)}">${DOC_ICON}${esc(s.title)}</span>`).join('');
      card.after(row);
    }
    meta.textContent = `Northbound Assistant · ${now()}`;
  }
  log.scrollTop = log.scrollHeight;
}

function showTyping() {
  const n = add('tpl-bot');
  const card = n.querySelector('.card');
  card.classList.add('typing');
  card.setAttribute('aria-label', 'Assistant is typing');
  card.innerHTML = '<span></span><span></span><span></span>';
  n.querySelector('.meta').remove();
  return n;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question || send.disabled) return;
  addUser(question);
  input.value = '';
  send.disabled = true;
  const typing = showTyping();
  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json().catch(() => ({ error: 'Unexpected response from the server.' }));
    typing.remove();
    addBot(res.ok ? data : { error: data.error || 'Please try again.' });
  } catch {
    typing.remove();
    addBot({ error: 'Can’t reach the assistant. Is the server running?' });
  } finally {
    send.disabled = false;
    input.focus();
  }
});

input.focus();
