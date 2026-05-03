from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(title="FastAPI Vercel Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ──────────────────────────────────────────────────────────────────

class EchoRequest(BaseModel):
    message: str

class EchoResponse(BaseModel):
    message: str
    reversed: str
    length: int
    timestamp: str

class RandomNumberRequest(BaseModel):
    max_value: int

class RandomNumberResponse(BaseModel):
    number: int
    min_value: int
    max_value: int
    timestamp: str

# ── HTML landing page ────────────────────────────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FastAPI · Vercel Demo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0a0f;
      --surface: #111118;
      --border: #232333;
      --accent: #7c6aff;
      --accent2: #ff6a9b;
      --text: #e8e8f0;
      --muted: #6b6b88;
      --success: #4fffb0;
      --mono: 'Space Mono', monospace;
      --sans: 'Syne', sans-serif;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 48px 24px;
    }

    /* animated grid bg */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 48px 48px;
      opacity: 0.35;
      pointer-events: none;
      z-index: 0;
    }

    .container { position: relative; z-index: 1; width: 100%; max-width: 720px; }

    header { margin-bottom: 48px; }
    .badge {
      display: inline-flex; align-items: center; gap: 6px;
      font-family: var(--mono); font-size: 11px;
      background: rgba(124,106,255,.15); border: 1px solid rgba(124,106,255,.3);
      color: var(--accent); padding: 4px 10px; border-radius: 99px;
      margin-bottom: 16px; letter-spacing: .08em;
    }
    .badge span { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

    h1 {
      font-size: clamp(2rem, 6vw, 3.5rem); font-weight: 800; line-height: 1.1;
      background: linear-gradient(135deg, #fff 30%, var(--accent));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .subtitle { color: var(--muted); margin-top: 10px; font-size: 1rem; font-family: var(--mono); }

    /* cards */
    .grid { display: grid; gap: 16px; margin-bottom: 24px; }
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 12px; padding: 24px;
      transition: border-color .2s;
    }
    .card:hover { border-color: var(--accent); }
    .card-title {
      font-family: var(--mono); font-size: 11px; letter-spacing: .12em;
      text-transform: uppercase; color: var(--muted); margin-bottom: 16px;
      display: flex; align-items: center; gap: 8px;
    }
    .card-title::before { content:''; display:block; width:3px; height:12px; background:var(--accent); border-radius:2px; }

    /* endpoint list */
    .ep { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); }
    .ep:last-child { border-bottom: none; }
    .method {
      font-family: var(--mono); font-size: 11px; font-weight: 700;
      padding: 3px 8px; border-radius: 4px; min-width: 44px; text-align: center;
    }
    .get  { background: rgba(79,255,176,.15); color: var(--success); border: 1px solid rgba(79,255,176,.2); }
    .post { background: rgba(124,106,255,.15); color: var(--accent);  border: 1px solid rgba(124,106,255,.2); }
    .ep-path { font-family: var(--mono); font-size: 13px; }
    .ep-desc { margin-left: auto; font-size: 12px; color: var(--muted); }

    /* try-it form */
    .input-row { display: flex; gap: 10px; }
    input[type=text] {
      flex: 1; background: var(--bg); border: 1px solid var(--border);
      color: var(--text); font-family: var(--mono); font-size: 13px;
      padding: 10px 14px; border-radius: 8px; outline: none;
      transition: border-color .2s;
    }
    input[type=text]:focus { border-color: var(--accent); }
    button {
      background: var(--accent); color: #fff; border: none; cursor: pointer;
      font-family: var(--sans); font-weight: 700; font-size: 13px;
      padding: 10px 20px; border-radius: 8px;
      transition: opacity .15s, transform .1s;
    }
    button:hover { opacity: .85; }
    button:active { transform: scale(.97); }
    button:disabled { opacity: .4; cursor: not-allowed; }

    .result-box {
      margin-top: 14px; background: var(--bg); border: 1px solid var(--border);
      border-radius: 8px; padding: 14px; font-family: var(--mono); font-size: 12px;
      line-height: 1.6; white-space: pre-wrap; min-height: 48px; color: var(--success);
      display: none;
    }
    .result-box.visible { display: block; }
    .error { color: var(--accent2) !important; }

    /* stats row */
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .stat { text-align: center; }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: var(--accent); }
    .stat-label { font-size: 11px; font-family: var(--mono); color: var(--muted); margin-top: 2px; }

    footer { margin-top: 40px; font-family: var(--mono); font-size: 11px; color: var(--muted); text-align: center; }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge"><span></span> LIVE ON VERCEL</div>
      <h1>FastAPI Demo</h1>
      <p class="subtitle">// serverless python · vercel runtime</p>
    </header>

    <div class="grid">
      <!-- endpoints -->
      <div class="card">
        <div class="card-title">Endpoints</div>
        <div class="ep">
          <span class="method get">GET</span>
          <span class="ep-path">/api/</span>
          <span class="ep-desc">This page</span>
        </div>
        <div class="ep">
          <span class="method get">GET</span>
          <span class="ep-path">/api/health</span>
          <span class="ep-desc">Health check</span>
        </div>
        <div class="ep">
          <span class="method get">GET</span>
          <span class="ep-path">/api/random-quote</span>
          <span class="ep-desc">Random quote</span>
        </div>
        <div class="ep">
          <span class="method post">POST</span>
          <span class="ep-path">/api/echo</span>
          <span class="ep-desc">Echo + transform</span>
        </div>
        <div class="ep">
          <span class="method post">POST</span>
          <span class="ep-path">/api/random-number</span>
          <span class="ep-desc">Random 0 to N</span>
        </div>
        <div class="ep">
          <span class="method get">GET</span>
          <span class="ep-path">/api/docs</span>
          <span class="ep-desc">Swagger UI</span>
        </div>
      </div>

      <!-- try it -->
      <div class="card">
        <div class="card-title">Try it — POST /api/echo</div>
        <div class="input-row">
          <input type="text" id="msg" placeholder="Type a message…" value="Hello from FastAPI Demo on Vercel!"/>
          <button id="sendBtn" onclick="tryEcho()">Send</button>
        </div>
        <div class="result-box" id="result"></div>
      </div>

      <!-- try random number -->
      <div class="card">
        <div class="card-title">Try it — POST /api/random-number</div>
        <div class="card-desc" style="color:var(--muted); font-size:12px; margin-bottom:12px;">Generate a random number between 0 and any upper bound you choose.</div>
        <div class="input-row">
          <input type="text" id="maxN" placeholder="Max value (e.g. 100)" value="100"/>
          <button id="rnBtn" onclick="tryRandomNumber()">Generate</button>
        </div>
        <div class="result-box" id="rnResult"></div>
      </div>

      <!-- stats -->
      <div class="card">
        <div class="card-title">Runtime info</div>
        <div class="stats">
          <div class="stat"><div class="stat-val" id="statPy">—</div><div class="stat-label">Python</div></div>
          <div class="stat"><div class="stat-val" id="statFa">—</div><div class="stat-label">FastAPI</div></div>
          <div class="stat"><div class="stat-val" id="statMs">—</div><div class="stat-label">Latency ms</div></div>
        </div>
      </div>
    </div>

    <footer>
      Built with FastAPI · Deployed on Vercel · <a href="/api/docs">Swagger UI →</a>
    </footer>
  </div>

  <script>
    async function tryEcho() {
      const btn = document.getElementById('sendBtn');
      const box = document.getElementById('result');
      const msg = document.getElementById('msg').value.trim();
      if (!msg) return;
      btn.disabled = true;
      box.className = 'result-box visible';
      box.textContent = 'Sending…';
      const t0 = performance.now();
      try {
        const res = await fetch('/echo', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        const ms = Math.round(performance.now() - t0);
        box.classList.remove('error');
        box.textContent = JSON.stringify(data, null, 2);
        document.getElementById('statMs').textContent = ms;
      } catch (e) {
        box.classList.add('error');
        box.textContent = 'Error: ' + e.message;
      } finally { btn.disabled = false; }
    }

    async function tryRandomNumber() {
      const btn = document.getElementById('rnBtn');
      const box = document.getElementById('rnResult');
      const maxN = parseInt(document.getElementById('maxN').value.trim(), 10);
      if (isNaN(maxN) || maxN < 0) return;
      btn.disabled = true;
      box.className = 'result-box visible';
      box.textContent = 'Generating…';
      try {
        const res = await fetch('/random-number', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ max_value: maxN })
        });
        const data = await res.json();
        box.classList.remove('error');
        box.textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        box.classList.add('error');
        box.textContent = 'Error: ' + e.message;
      } finally { btn.disabled = false; }
    }

    async function loadHealth() {
      try {
        const res = await fetch('/health');
        const d = await res.json();
        document.getElementById('statPy').textContent = d.python_version?.split('.').slice(0,2).join('.') ?? '—';
        document.getElementById('statFa').textContent = d.fastapi_version ?? '—';
      } catch {}
    }

    document.getElementById('msg').addEventListener('keydown', e => {
      if (e.key === 'Enter') tryEcho();
    });

    document.getElementById('maxN').addEventListener('keydown', e => {
      if (e.key === 'Enter') tryRandomNumber();
    });

    loadHealth();
  </script>
</body>
</html>
"""

# ── Routes ────────────────────────────────────────────────────────────────────

QUOTES = [
    "Simplicity is the soul of efficiency. — Austin Freeman",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Code is like humor. When you have to explain it, it's bad. — Cory House",
    "Make it work, make it right, make it fast. — Kent Beck",
    "Programs must be written for people to read. — Abelson & Sussman",
]

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML

@app.get("/health")
async def health():
    import sys, fastapi
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "python_version": sys.version,
        "fastapi_version": fastapi.__version__,
    }

@app.get("/random-quote")
async def random_quote():
    quote = random.choice(QUOTES)
    author = quote.split("— ")[-1] if "— " in quote else "Unknown"
    text = quote.split(" — ")[0] if " — " in quote else quote
    return {"quote": text, "author": author, "timestamp": datetime.utcnow().isoformat() + "Z"}

@app.post("/echo", response_model=EchoResponse)
async def echo(body: EchoRequest):
    return EchoResponse(
        message=body.message,
        reversed=body.message[::-1],
        length=len(body.message),
        timestamp=datetime.utcnow().isoformat() + "Z",
    )

@app.post("/random-number", response_model=RandomNumberResponse)
async def random_number(body: RandomNumberRequest):
    return RandomNumberResponse(
        number=random.randint(0, body.max_value),
        min_value=0,
        max_value=body.max_value,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
