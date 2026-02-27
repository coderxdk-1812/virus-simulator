import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Virus Spread Simulation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background: #070d1a; }
</style>
""", unsafe_allow_html=True)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:#070d1a; --panel:#0c1425; --card:#101c30; --border:#1a2e4a;
    --accent:#00d4ff; --sick:#ff3d5a; --immune:#00e5a0; --healthy:#4a9eff;
    --total:#e0e8ff; --text:#b8cce8; --dim:#3d5070;
    --mono:'Share Tech Mono',monospace;
  }
  body {
    font-family:'Rajdhani',sans-serif;
    background:var(--bg); color:var(--text);
    height:860px; overflow:hidden;
    display:flex; flex-direction:column;
  }

  /* HEADER */
  .hdr {
    background:var(--panel); border-bottom:1px solid var(--border);
    padding:7px 20px; display:flex; align-items:center; gap:12px; flex-shrink:0;
  }
  .pulse {
    width:8px; height:8px; border-radius:50%;
    background:var(--immune); box-shadow:0 0 8px var(--immune);
    animation:blink 2s infinite; flex-shrink:0;
  }
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
  .h-title { font-family:var(--mono); font-size:15px; color:var(--accent); letter-spacing:3px; }
  .h-sub   { font-size:11px; color:var(--dim); letter-spacing:2px; margin-left:auto; }

  /* LAYOUT */
  .layout { display:flex; flex:1; overflow:hidden; }

  /* LEFT */
  .lp {
    width:240px; min-width:240px;
    background:var(--panel); border-right:1px solid var(--border);
    display:flex; flex-direction:column; padding:14px 16px; gap:12px; overflow-y:auto;
  }
  .sec {
    font-family:var(--mono); font-size:9px; color:var(--accent);
    letter-spacing:2px; text-transform:uppercase;
    border-bottom:1px solid var(--border); padding-bottom:5px;
  }
  .param { display:flex; flex-direction:column; gap:4px; }
  .param-top { display:flex; justify-content:space-between; align-items:center; }
  .param-name { font-size:13px; font-weight:700; color:var(--text); }
  .param-val  { font-family:var(--mono); font-size:13px; color:var(--accent); }

  /* Slider */
  input[type=range] {
    -webkit-appearance:none; appearance:none;
    width:100%; height:4px; border-radius:2px;
    background:transparent; outline:none; cursor:pointer; display:block;
  }
  input[type=range]::-webkit-slider-runnable-track {
    height:4px; border-radius:2px;
    background:linear-gradient(to right,var(--accent) 0%,var(--accent) var(--pct,0%),var(--border) var(--pct,0%));
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance:none;
    width:18px; height:18px; margin-top:-7px;
    border-radius:50%; background:var(--accent);
    box-shadow:0 0 8px var(--accent); cursor:pointer;
  }
  input[type=range]::-moz-range-track { height:4px; border-radius:2px; background:var(--border); }
  input[type=range]::-moz-range-progress { height:4px; border-radius:2px; background:var(--accent); }
  input[type=range]::-moz-range-thumb {
    width:18px; height:18px; border:none; border-radius:50%;
    background:var(--accent); box-shadow:0 0 8px var(--accent); cursor:pointer;
  }

  /* Shapes */
  .shapes { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
  .shape-btn {
    padding:8px; border:1px solid var(--border); border-radius:5px;
    background:var(--card); color:var(--dim); font-size:18px;
    cursor:pointer; text-align:center; transition:all .15s;
  }
  .shape-btn:hover  { border-color:var(--accent); color:var(--accent); }
  .shape-btn.active {
    border-color:var(--accent); background:rgba(0,212,255,.1);
    color:var(--accent); box-shadow:0 0 8px rgba(0,212,255,.2);
  }
  .gap { flex:1; }
  .btn-setup {
    padding:9px; width:100%; border:1px solid var(--border); border-radius:6px;
    background:var(--card); color:var(--dim); font-family:var(--mono);
    font-size:11px; letter-spacing:2px; cursor:pointer; transition:all .2s;
  }
  .btn-setup:hover { border-color:var(--accent); color:var(--text); }
  .btn-go {
    padding:13px; width:100%; border:2px solid var(--accent); border-radius:7px;
    background:rgba(0,212,255,.07); color:var(--accent); font-family:var(--mono);
    font-size:16px; letter-spacing:5px; cursor:pointer; transition:all .2s;
    box-shadow:0 0 12px rgba(0,212,255,.2);
  }
  .btn-go:hover { background:rgba(0,212,255,.18); box-shadow:0 0 22px rgba(0,212,255,.45); }
  .btn-go.on    { border-color:var(--sick); color:var(--sick); background:rgba(255,61,90,.07); box-shadow:0 0 12px rgba(255,61,90,.25); }

  /* SIM */
  .sim-area {
    flex:1; position:relative; overflow:hidden; background:var(--bg);
  }
  .sim-area::before {
    content:''; position:absolute; inset:0;
    background-image:
      linear-gradient(rgba(26,46,74,.18) 1px,transparent 1px),
      linear-gradient(90deg,rgba(26,46,74,.18) 1px,transparent 1px);
    background-size:44px 44px; pointer-events:none; z-index:1;
  }
  #simCanvas { width:100%; height:100%; display:block; }
  .legend {
    position:absolute; bottom:12px; left:50%; transform:translateX(-50%);
    display:flex; gap:18px; background:rgba(7,13,26,.9);
    border:1px solid var(--border); border-radius:7px; padding:7px 20px; z-index:2;
  }
  .leg     { display:flex; align-items:center; gap:7px; font-size:12px; font-weight:700; }
  .leg-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }

  /* RIGHT */
  .rp {
    width:340px; min-width:340px;
    background:var(--panel); border-left:1px solid var(--border);
    display:flex; flex-direction:column; padding:14px 16px; gap:10px; overflow:hidden;
  }
  .stats-row { display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; flex-shrink:0; }
  .stat { background:var(--card); border:1px solid var(--border); border-radius:7px; padding:9px 10px; }
  .stat-lbl { font-family:var(--mono); font-size:8px; color:var(--dim); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:3px; }
  .stat-val { font-family:var(--mono); font-size:20px; font-weight:700; line-height:1; }
  .stat-bar { height:3px; background:var(--border); border-radius:2px; overflow:hidden; margin-top:5px; }
  .stat-bar-fill { height:100%; border-radius:2px; transition:width .4s; }

  .graph-title {
    font-family:var(--mono); font-size:10px; color:var(--accent);
    letter-spacing:2px; text-transform:uppercase;
    border-bottom:1px solid var(--border); padding-bottom:5px; flex-shrink:0;
  }
  #graphCanvas {
    flex:1; width:100%; min-height:0; display:block;
    border:1px solid var(--border); border-radius:7px; background:var(--card);
  }
  .graph-key { display:grid; grid-template-columns:1fr 1fr; gap:4px 10px; flex-shrink:0; }
  .gk      { display:flex; align-items:center; gap:7px; font-size:12px; font-weight:700; }
  .gk-line { width:22px; height:3px; border-radius:2px; flex-shrink:0; }
</style>
</head>
<body>

<div class="hdr">
  <div class="pulse"></div>
  <div class="h-title">VIRUSIM // SIR Biological Spread</div>
  <div class="h-sub">NetLogo Virus Biology — Interactive</div>
</div>

<div class="layout">

  <!-- LEFT CONTROLS -->
  <div class="lp">
    <div class="sec">Parameters</div>
    <div class="param">
      <div class="param-top"><span class="param-name">Model Speed</span><span class="param-val" id="vSpd">5</span></div>
      <input type="range" id="speed" min="1" max="10" value="5">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Population</span><span class="param-val" id="vPop">100</span></div>
      <input type="range" id="population" min="10" max="300" value="100" step="5">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Infectiousness</span><span class="param-val" id="vInf">65%</span></div>
      <input type="range" id="infectiousness" min="0" max="100" value="65">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Chance Recover</span><span class="param-val" id="vRec">25%</span></div>
      <input type="range" id="chanceRecover" min="0" max="100" value="25">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Duration (wks)</span><span class="param-val" id="vDur">20</span></div>
      <input type="range" id="duration" min="1" max="100" value="20">
    </div>

    <div class="sec" style="margin-top:2px">Agent Shape</div>
    <div class="shapes">
      <button class="shape-btn active" data-shape="person">🧍</button>
      <button class="shape-btn" data-shape="circle">⬤</button>
      <button class="shape-btn" data-shape="triangle">▲</button>
      <button class="shape-btn" data-shape="diamond">◆</button>
    </div>

    <div class="gap"></div>
    <button class="btn-setup" id="btnSetup">[ SETUP ]</button>
    <button class="btn-go"    id="btnGo">▶  GO</button>
  </div>

  <!-- CENTER SIM -->
  <div class="sim-area">
    <canvas id="simCanvas"></canvas>
    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:var(--healthy);box-shadow:0 0 6px var(--healthy)"></div>Susceptible</div>
      <div class="leg"><div class="leg-dot" style="background:var(--sick);box-shadow:0 0 6px var(--sick)"></div>Infected</div>
      <div class="leg"><div class="leg-dot" style="background:var(--immune);box-shadow:0 0 6px var(--immune)"></div>Recovered</div>
    </div>
  </div>

  <!-- RIGHT STATS + GRAPH -->
  <div class="rp">
    <div class="sec">Live Stats</div>
    <div class="stats-row">
      <div class="stat">
        <div class="stat-lbl">Infected</div>
        <div class="stat-val" id="sInf" style="color:var(--sick)">0%</div>
        <div class="stat-bar"><div class="stat-bar-fill" id="bInf" style="background:var(--sick);width:0%"></div></div>
      </div>
      <div class="stat">
        <div class="stat-lbl">Immune</div>
        <div class="stat-val" id="sImm" style="color:var(--immune)">0%</div>
        <div class="stat-bar"><div class="stat-bar-fill" id="bImm" style="background:var(--immune);width:0%"></div></div>
      </div>
      <div class="stat">
        <div class="stat-lbl">Time</div>
        <div class="stat-val" id="sTime" style="color:var(--accent)">0.0y</div>
      </div>
    </div>

    <div class="graph-title">SIR Population Graph</div>
    <canvas id="graphCanvas"></canvas>
    <div class="graph-key">
      <div class="gk"><div class="gk-line" style="background:var(--sick)"></div>Infected (I)</div>
      <div class="gk"><div class="gk-line" style="background:var(--immune)"></div>Recovered (R)</div>
      <div class="gk"><div class="gk-line" style="background:var(--healthy)"></div>Susceptible (S)</div>
      <div class="gk"><div class="gk-line" style="background:var(--total)"></div>Total</div>
    </div>
  </div>

</div>

<script>
// ─── CONFIG ───────────────────────────────────────────────
const CONTACT_R = 12;          // infection radius (px)
const CELL_SIZE  = CONTACT_R * 2; // spatial grid cell size
const MAX_HIST   = 350;        // graph history length
const TICKS_PER_FRAME = 1;     // ONE tick per animation frame — never pile up

// ─── REFS ─────────────────────────────────────────────────
const SIM = document.getElementById('simCanvas');
const GRP = document.getElementById('graphCanvas');
const sCtx = SIM.getContext('2d');
const gCtx = GRP.getContext('2d');

// ─── STATE ────────────────────────────────────────────────
let agents = [], running = false, raf = null, tick = 0;
let hist = { s:[], i:[], r:[], t:[] };
let agentShape = 'person';

const P = id => parseFloat(document.getElementById(id).value);

// ─── RESIZE ───────────────────────────────────────────────
function resize() {
  const area = document.querySelector('.sim-area');
  SIM.width  = area.clientWidth;
  SIM.height = area.clientHeight;
  GRP.width  = GRP.clientWidth;
  GRP.height = GRP.clientHeight;
}
window.addEventListener('resize', () => { resize(); drawGraph(); });
resize();

// ─── SPATIAL GRID (avoid O(n²) per frame) ─────────────────
function buildGrid(W, H) {
  const cols = Math.ceil(W / CELL_SIZE);
  const rows = Math.ceil(H / CELL_SIZE);
  const grid = new Array(cols * rows);
  for (let k = 0; k < grid.length; k++) grid[k] = [];
  for (const a of agents) {
    const col = Math.floor(a.x / CELL_SIZE);
    const row = Math.floor(a.y / CELL_SIZE);
    const idx = row * cols + col;
    if (grid[idx]) grid[idx].push(a);
  }
  return { grid, cols, rows };
}

function getNeighbours(grid, cols, rows, cx, cy) {
  const out = [];
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      const r = cy + dr, c = cx + dc;
      if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
      const cell = grid[r * cols + c];
      if (cell) for (const a of cell) out.push(a);
    }
  }
  return out;
}

// ─── AGENT ────────────────────────────────────────────────
class Agent {
  constructor(x, y, state) {
    this.x = x; this.y = y; this.state = state;
    this.angle = Math.random() * Math.PI * 2;
    this.speed = 0.8 + Math.random() * 0.8;
    this.infectedAt = state === 'I' ? 0 : -1;
  }

  move(W, H) {
    this.angle += (Math.random() - 0.5) * 0.7;
    this.x += Math.cos(this.angle) * this.speed;
    this.y += Math.sin(this.angle) * this.speed;
    if (this.x < 0)  this.x += W;
    if (this.x > W)  this.x -= W;
    if (this.y < 0)  this.y += H;
    if (this.y > H)  this.y -= H;
  }

  draw(ctx) {
    const col = this.state==='I' ? '#ff3d5a'
               : this.state==='R' ? '#00e5a0'
               : '#4a9eff';
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.fillStyle = col;
    ctx.strokeStyle = col;
    ctx.shadowColor = col;
    ctx.shadowBlur  = 6;
    const s = 6;

    if (agentShape === 'person') {
      ctx.beginPath(); ctx.arc(0, -s*1.55, s*0.62, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.rect(-s*.42, -s*.88, s*.84, s*1.3); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(-s*.22, s*.42); ctx.lineTo(-s*.48, s*1.4);
      ctx.moveTo( s*.22, s*.42); ctx.lineTo( s*.48, s*1.4);
      ctx.lineWidth = s*.42; ctx.lineCap = 'round'; ctx.stroke();
    } else if (agentShape === 'circle') {
      ctx.beginPath(); ctx.arc(0, 0, s*.7, 0, Math.PI*2); ctx.fill();
    } else if (agentShape === 'triangle') {
      ctx.beginPath();
      ctx.moveTo(0,-s); ctx.lineTo(s*.87,s*.5); ctx.lineTo(-s*.87,s*.5);
      ctx.closePath(); ctx.fill();
    } else {
      ctx.beginPath();
      ctx.moveTo(0,-s*.95); ctx.lineTo(s*.6,0);
      ctx.lineTo(0,s*.95);  ctx.lineTo(-s*.6,0);
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  }
}

// ─── SETUP ────────────────────────────────────────────────
function setup() {
  if (running) stop();
  tick = 0;
  hist = { s:[], i:[], r:[], t:[] };
  agents = [];
  const n = Math.round(P('population'));
  const W = SIM.width, H = SIM.height;
  for (let k = 0; k < n; k++) {
    const x = 16 + Math.random() * (W - 32);
    const y = 16 + Math.random() * (H - 32);
    agents.push(new Agent(x, y, k === 0 ? 'I' : 'S'));
  }
  drawSim();
  drawGraph();
  updateStats();
}

// ─── ONE TICK ─────────────────────────────────────────────
function doTick() {
  const W = SIM.width, H = SIM.height;
  const infectP = P('infectiousness') / 100;
  const recoverP = P('chanceRecover')  / 100;
  const dur      = P('duration');
  const R2       = CONTACT_R * CONTACT_R;

  // 1. Move all agents
  for (const a of agents) a.move(W, H);

  // 2. Build spatial grid once per tick
  const { grid, cols, rows } = buildGrid(W, H);

  // 3. Infection + recovery — O(n * ~9 cells) not O(n²)
  for (const inf of agents) {
    if (inf.state !== 'I') continue;

    // Infect nearby susceptibles
    const cx = Math.floor(inf.x / CELL_SIZE);
    const cy = Math.floor(inf.y / CELL_SIZE);
    const nbrs = getNeighbours(grid, cols, rows, cx, cy);
    for (const other of nbrs) {
      if (other === inf || other.state !== 'S') continue;
      const dx = inf.x - other.x, dy = inf.y - other.y;
      if (dx*dx + dy*dy < R2 && Math.random() < infectP) {
        other.state = 'I';
        other.infectedAt = tick;
      }
    }

    // Recovery
    if ((tick - inf.infectedAt) >= dur && Math.random() < recoverP) {
      inf.state = 'R';
    }
  }

  tick++;

  // 4. Record history every 3 ticks
  if (tick % 3 === 0) {
    const nI = agents.filter(a => a.state==='I').length;
    const nR = agents.filter(a => a.state==='R').length;
    const nS = agents.length - nI - nR;
    hist.i.push(nI); hist.r.push(nR); hist.s.push(nS); hist.t.push(agents.length);
    if (hist.i.length > MAX_HIST) {
      hist.i.shift(); hist.r.shift(); hist.s.shift(); hist.t.shift();
    }
  }
}

// ─── DRAW SIM ─────────────────────────────────────────────
function drawSim() {
  sCtx.fillStyle = '#070d1a';
  sCtx.fillRect(0, 0, SIM.width, SIM.height);
  for (const a of agents) a.draw(sCtx);
}

// ─── DRAW GRAPH ───────────────────────────────────────────
function drawGraph() {
  const W = GRP.width, H = GRP.height;
  gCtx.fillStyle = '#101c30';
  gCtx.fillRect(0, 0, W, H);

  const n = hist.i.length;
  if (n < 2) return;

  const pad = { t:12, b:26, l:34, r:10 };
  const gW  = W - pad.l - pad.r;
  const gH  = H - pad.t - pad.b;
  const maxY = agents.length || 1;

  // Grid lines + y labels
  gCtx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + (i/4) * gH;
    gCtx.strokeStyle = 'rgba(26,46,74,.9)';
    gCtx.beginPath(); gCtx.moveTo(pad.l, y); gCtx.lineTo(W-pad.r, y); gCtx.stroke();
    gCtx.fillStyle = 'rgba(61,80,112,.95)';
    gCtx.font = '9px Share Tech Mono';
    gCtx.textAlign = 'right';
    gCtx.fillText(Math.round(maxY*(1-i/4)), pad.l-4, y+3);
  }

  // x labels (years)
  gCtx.fillStyle = 'rgba(61,80,112,.8)';
  gCtx.font = '8px Share Tech Mono';
  gCtx.textAlign = 'center';
  for (let i = 0; i <= 4; i++) {
    const x = pad.l + (i/4)*gW;
    const yr = (i/4 * n*3 / 52).toFixed(1);
    gCtx.fillText(yr+'y', x, H-pad.b+14);
  }

  // Plot a line
  function line(arr, color, lw) {
    if (arr.length < 2) return;
    gCtx.beginPath();
    gCtx.strokeStyle = color;
    gCtx.lineWidth   = lw || 2;
    gCtx.shadowColor = color;
    gCtx.shadowBlur  = 5;
    gCtx.lineJoin    = 'round';
    arr.forEach((v, i) => {
      const x = pad.l + (i/(arr.length-1))*gW;
      const y = pad.t + gH - (v/maxY)*gH;
      i === 0 ? gCtx.moveTo(x, y) : gCtx.lineTo(x, y);
    });
    gCtx.stroke();
    gCtx.shadowBlur = 0;
  }

  line(hist.t, '#e0e8ff', 1.5);
  line(hist.s, '#4a9eff', 2);
  line(hist.r, '#00e5a0', 2);
  line(hist.i, '#ff3d5a', 2.5);
}

// ─── STATS ────────────────────────────────────────────────
function updateStats() {
  const total = agents.length || 1;
  const nI = agents.filter(a => a.state==='I').length;
  const nR = agents.filter(a => a.state==='R').length;
  const pI = (nI/total*100).toFixed(1);
  const pR = (nR/total*100).toFixed(1);
  document.getElementById('sInf').textContent  = pI + '%';
  document.getElementById('sImm').textContent  = pR + '%';
  document.getElementById('sTime').textContent = (tick/52).toFixed(1) + 'y';
  document.getElementById('bInf').style.width  = pI + '%';
  document.getElementById('bImm').style.width  = pR + '%';
}

// ─── MAIN LOOP — exactly 1 tick per frame, no accumulator ──
function loop() {
  if (!running) return;

  // Speed slider scales target FPS via setTimeout-gating
  const targetFPS = P('speed') * 3;  // 3–30 fps
  doTick();
  drawSim();
  drawGraph();
  updateStats();

  raf = setTimeout(() => requestAnimationFrame(loop), 1000 / targetFPS);
}

function start() {
  if (running) return;
  if (agents.length === 0) setup();
  running = true;
  document.getElementById('btnGo').textContent = '⏸  PAUSE';
  document.getElementById('btnGo').classList.add('on');
  raf = requestAnimationFrame(loop);
}

function stop() {
  running = false;
  clearTimeout(raf);
  if (raf) cancelAnimationFrame(raf);
  document.getElementById('btnGo').textContent = '▶  GO';
  document.getElementById('btnGo').classList.remove('on');
}

// ─── BUTTONS ──────────────────────────────────────────────
document.getElementById('btnGo').addEventListener('click', () => {
  running ? stop() : start();
});
document.getElementById('btnSetup').addEventListener('click', () => {
  setup();
});

// ─── SLIDERS ──────────────────────────────────────────────
function bindSlider(id, valId, suffix) {
  const el = document.getElementById(id);
  const vl = document.getElementById(valId);
  function update() {
    vl.textContent = el.value + (suffix||'');
    const pct = (el.value-el.min)/(el.max-el.min)*100;
    el.style.setProperty('--pct', pct+'%');
  }
  el.addEventListener('input', update);
  update();
}
bindSlider('speed',          'vSpd', '');
bindSlider('population',     'vPop', '');
bindSlider('infectiousness', 'vInf', '%');
bindSlider('chanceRecover',  'vRec', '%');
bindSlider('duration',       'vDur', '');

// ─── SHAPES ───────────────────────────────────────────────
document.querySelectorAll('.shape-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.shape-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    agentShape = btn.dataset.shape;
  });
});

// ─── INIT ─────────────────────────────────────────────────
setup();
</script>
</body>
</html>"""

components.html(HTML, height=860, scrolling=False)
