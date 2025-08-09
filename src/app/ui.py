from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response

router = APIRouter()

HTML = """
<!doctype html>
<html lang="es" data-color-scheme="auto">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Clara — Tutora de Español Médico</title>
  <meta name="description" content="Práctica de Español médico en un entorno cómodo y seguro." />
  <style>
    /* ------------------------------------------------------
       Apple-inspired UI: calm, tactile, and precise
       - System font stack emphasizes SF Pro on Apple devices
       - Large, airy spacing; subtle depth; gentle motion
       ------------------------------------------------------ */
    :root {
      --bg: #f5f7fb;
      --card: #ffffffcc;
      --ink: #0b0c0e;
      --muted: #5b616e;
      --tint: #0a84ff; /* iOS blue */
      --border: rgba(0,0,0,.08);
      --radius: 18px;
      --shadow-1: 0 1px 3px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.06);
      --shadow-2: 0 10px 30px rgba(0,0,0,.10);
      --me: #e7f1ff;    /* my bubbles */
      --ai: #f2f3f6;    /* tutor bubbles */
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #0b0c0f;
        --card: #14161acc;
        --ink: #f2f4f8;
        --muted: #c2c7d0;
        --tint: #0a84ff;
        --border: rgba(255,255,255,.08);
        --me: #0f253f;
        --ai: #171a21;
      }
      body { color-scheme: dark; }
    }
    html,body { height: 100%; }
    body {
      margin: 0;
      font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, system-ui, "Apple Color Emoji", "Segoe UI Emoji";
      color: var(--ink);
      background:
        radial-gradient(1200px 600px at 10% -10%, rgba(10,132,255,.08), transparent),
        radial-gradient(800px 500px at 100% 0%, rgba(88,86,214,.06), transparent),
        var(--bg);
    }
    .wrap {
      max-width: 920px;
      margin: clamp(16px,3vw,36px) auto;
      padding: 0 clamp(12px,2vw,24px);
    }
    .card {
      backdrop-filter: saturate(1.2) blur(10px);
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: calc(var(--radius) * 1.2);
      box-shadow: var(--shadow-1);
      overflow: clip;
    }
    header.hero {
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 16px;
      align-items: center;
      padding: 18px 20px;
      border-bottom: 1px solid var(--border);
      background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(255,255,255,0));
    }
    @media (prefers-color-scheme: dark) {
      header.hero { background: linear-gradient(180deg, rgba(20,22,26,.7), rgba(20,22,26,0)); }
    }
    .avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg,#c2e0ff,#b3ffd8); border:1px solid var(--border); box-shadow: var(--shadow-1); }
    .title { font-size: 20px; font-weight: 700; letter-spacing: .2px; }
    .sub { color: var(--muted); font-size: 14px; margin-top: 2px; }

    .controls { display: flex; gap: 12px; align-items: center; }
    .select {
      display: grid; gap: 2px; font-size: 12px; color: var(--muted);
    }
    .select select {
      appearance: none; -webkit-appearance: none; -moz-appearance: none;
      background: rgba(127,127,127,.06);
      border: 1px solid var(--border);
      color: var(--ink);
      padding: 8px 12px;
      border-radius: 12px;
      outline: none;
    }
    .select select:focus { box-shadow: 0 0 0 3px rgba(10,132,255,.20); border-color: rgba(10,132,255,.55); }

    /* Chat area */
    .chat {
      height: min(62vh, 560px);
      overflow: auto;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      scroll-behavior: smooth;
      background: linear-gradient(180deg, transparent, rgba(0,0,0,.02));
    }
    .row { display: grid; grid-template-columns: 1fr; }
    .row.me { justify-items: end; }
    .bubble {
      max-width: 85ch;
      padding: 10px 14px;
      border-radius: 16px;
      border: 1px solid var(--border);
      box-shadow: 0 1px 0 rgba(0,0,0,.04);
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    .me .bubble { background: var(--me); }
    .ai .bubble { background: var(--ai); }
    .meta { font-size: 12px; color: var(--muted); margin: 2px 6px 0; }

    /* Composer */
    .composer {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: end;
      padding: 16px;
      border-top: 1px solid var(--border);
      background: linear-gradient(0deg, rgba(0,0,0,.02), transparent);
    }
    .field {
      display: grid; gap: 8px;
    }
    textarea {
      resize: none; min-height: 54px; max-height: 30vh;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 14px;
      font: inherit; color: inherit; background: transparent;
      outline: none;
    }
    textarea:focus { box-shadow: 0 0 0 3px rgba(10,132,255,.20); border-color: rgba(10,132,255,.55); }

    .actions { display: flex; gap: 8px; }
    .btn {
      display: inline-flex; align-items: center; gap: 8px;
      height: 44px; padding: 0 16px; border-radius: 14px;
      border: 1px solid var(--border); background: #ffffffaa;
      cursor: pointer; user-select: none;
      transition: transform .06s ease, box-shadow .2s ease;
    }
    @media (prefers-color-scheme: dark) {
      .btn { background: #1b1d22aa; }
    }
    .btn.primary { background: linear-gradient(180deg, #0a84ff, #0066cc); color: white; border: none; box-shadow: 0 8px 20px rgba(10,132,255,.35); }
    .btn:active { transform: translateY(1px); }
    .btn[disabled] { opacity: .6; cursor: not-allowed; box-shadow: none; }

    .typing { display: none; align-items: center; gap: 8px; color: var(--muted); }
    .typing.on { display: inline-flex; }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; opacity: .6; animation: pulse 1.2s infinite ease-in-out; }
    .dot:nth-child(2){ animation-delay: .15s }
    .dot:nth-child(3){ animation-delay: .3s }
    @keyframes pulse { 0%,80%,100%{ transform: translateY(0); opacity:.3 } 40%{ transform: translateY(-3px); opacity:.9 } }

    /* Accessibility: reduced motion */
    @media (prefers-reduced-motion: reduce){
      .chat { scroll-behavior: auto; }
      .btn { transition: none; }
      .dot { animation: none; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="card" role="application" aria-label="Tutor de Español médico">
      <header class="hero">
        <div class="avatar" aria-hidden="true"></div>
        <div>
          <div class="title">Clara</div>
          <div class="sub">Práctica cómoda, correcciones suaves. Sin consejos médicos reales.</div>
        </div>
        <div class="controls" aria-label="Controles">
          <div class="select"><label for="scenario">Escenario</label>
            <select id="scenario" name="scenario" aria-label="Seleccionar escenario">
              <option value="urgent_care_triage">Triage</option>
              <option value="hpi_basic">Historia clínica (HPI)</option>
              <option value="discharge_instructions">Instrucciones de alta</option>
            </select>
          </div>
          <div class="select"><label for="level">Nivel</label>
            <select id="level" name="level" aria-label="Seleccionar nivel">
              <option value="A2">A2</option>
              <option value="B1" selected>B1</option>
              <option value="B2">B2</option>
            </select>
          </div>
        </div>
      </header>

      <div id="chat" class="chat" role="log" aria-live="polite" aria-relevant="additions"></div>

      <div class="composer">
        <div class="field">
          <label class="sub" for="msg">Mensaje</label>
          <textarea id="msg" placeholder="Escribe aquí… (⌘/Ctrl + Enter para enviar)" rows="2"></textarea>
          <span id="typing" class="typing" aria-live="polite"><span class="dot"></span><span class="dot"></span><span class="dot"></span> Clara está escribiendo…</span>
        </div>
        <div class="actions">
          <button id="send" class="btn primary" aria-label="Enviar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 11.5l17-8-7 8 7 8-17-8z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
            Enviar
          </button>
        </div>
      </div>
    </section>
  </div>

  <script>
    const chat = document.getElementById('chat');
    const msg = document.getElementById('msg');
    const send = document.getElementById('send');
    const typing = document.getElementById('typing');
    const scenario = document.getElementById('scenario');
    const level = document.getElementById('level');

    function add(role, text){
      const row = document.createElement('div');
      row.className = 'row ' + role;
      const bubble = document.createElement('div');
      bubble.className = 'bubble';
      bubble.textContent = text;
      row.appendChild(bubble);
      chat.appendChild(row);
      chat.scrollTop = chat.scrollHeight;
    }

    async function sendMessage(){
      const text = msg.value.trim();
      if(!text) return;
      add('me', text);
      msg.value = '';
      send.disabled = true; typing.classList.add('on');
      try {
        const r = await fetch('/chat', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user: text, scenario: scenario.value, level: level.value })
        });
        const j = await r.json();
        add('ai', j.reply || '…');
      } catch (e) {
        add('ai', 'Error de red. Intenta de nuevo.');
      } finally {
        send.disabled = false; typing.classList.remove('on'); msg.focus();
      }
    }

    // Button click
    send.addEventListener('click', (e)=>{ e.preventDefault(); sendMessage(); });
    // Cmd/Ctrl + Enter to send
    msg.addEventListener('keydown', (e)=>{
      if ((e.key === 'Enter' && (e.metaKey || e.ctrlKey))) { e.preventDefault(); sendMessage(); }
    });
    // Focus ready
    window.addEventListener('load', ()=> msg.focus());

    // Warm greeting
    add('ai', 'Hola, soy Clara. ¿Qué te trae hoy? Podemos practicar triage, HPI o instrucciones de alta.');
  </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def home(_: Request):
  return HTML

# Tiny inlined favicon to avoid 404s (a 1x1 transparent PNG)
@router.get("/favicon.ico")
def favicon():
  data = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAuMBg4wV9bwAAAAASUVORK5CYII='
  return Response(content=data, media_type="image/png")
