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
    --accent:#00d4ff; --sick:#ff3d5a; --immune:#8899bb; --healthy:#00cc44;
    --total:#e0e8ff; --text:#b8cce8; --dim:#3d5070;
    --mono:'Share Tech Mono',monospace;
  }
  body {
    font-family:'Rajdhani',sans-serif;
    background:var(--bg); color:var(--text);
    height:860px; overflow:hidden;
    display:flex; flex-direction:column;
  }
  .hdr {
    background:var(--panel); border-bottom:1px solid var(--border);
    padding:7px 20px; display:flex; align-items:center; gap:12px; flex-shrink:0;
  }
  .pulse {
    width:8px; height:8px; border-radius:50%;
    background:var(--healthy); box-shadow:0 0 8px var(--healthy);
    animation:blink 2s infinite; flex-shrink:0;
  }
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
  .h-title { font-family:var(--mono); font-size:15px; color:var(--accent); letter-spacing:3px; }
  .h-sub   { font-size:11px; color:var(--dim); letter-spacing:2px; margin-left:auto; }

  .layout { display:flex; flex:1; overflow:hidden; }

  /* LEFT */
  .lp {
    width:245px; min-width:245px;
    background:var(--panel); border-right:1px solid var(--border);
    display:flex; flex-direction:column; padding:14px 16px; gap:11px; overflow-y:auto;
  }
  .sec {
    font-family:var(--mono); font-size:9px; color:var(--accent);
    letter-spacing:2px; text-transform:uppercase;
    border-bottom:1px solid var(--border); padding-bottom:5px;
  }
  .param { display:flex; flex-direction:column; gap:5px; }
  .param-top { display:flex; justify-content:space-between; align-items:center; }
  .param-name { font-size:13px; font-weight:700; color:var(--text); }
  .param-val  { font-family:var(--mono); font-size:13px; color:var(--accent); }

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

  .shapes { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
  .shape-btn {
    padding:8px; border:1px solid var(--border); border-radius:5px;
    background:var(--card); color:var(--dim); font-size:18px;
    cursor:pointer; text-align:center; transition:all .15s;
  }
  .shape-btn:hover  { border-color:var(--accent); color:var(--accent); }
  .shape-btn.active { border-color:var(--accent); background:rgba(0,212,255,.1); color:var(--accent); box-shadow:0 0 8px rgba(0,212,255,.2); }

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
      linear-gradient(rgba(26,46,74,.15) 1px,transparent 1px),
      linear-gradient(90deg,rgba(26,46,74,.15) 1px,transparent 1px);
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
    width:360px; min-width:360px;
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
  .graph-key { display:grid; grid-template-columns:1fr 1fr; gap:5px 12px; flex-shrink:0; }
  .gk      { display:flex; align-items:center; gap:7px; font-size:12px; font-weight:700; }
  .gk-line { width:22px; height:3px; border-radius:2px; flex-shrink:0; }
</style>
</head>
<body>

<div class="hdr">
  <div class="pulse"></div>
  <div class="h-title">VIRUSIM // SIR Biological Spread</div>
  <div class="h-sub">NetLogo Virus Biology — Faithful Replica</div>
</div>

<div class="layout">

  <div class="lp">
    <div class="sec">Parameters</div>

    <div class="param">
      <div class="param-top"><span class="param-name">Model Speed</span><span class="param-val" id="vSpd">5</span></div>
      <input type="range" id="speed" min="1" max="10" value="5">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Number of People</span><span class="param-val" id="vPop">150</span></div>
      <input type="range" id="population" min="10" max="300" value="150" step="5">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Infectiousness</span><span class="param-val" id="vInf">65%</span></div>
      <input type="range" id="infectiousness" min="0" max="100" value="65">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Chance Recover</span><span class="param-val" id="vRec">75%</span></div>
      <input type="range" id="chanceRecover" min="0" max="100" value="75">
    </div>
    <div class="param">
      <div class="param-top"><span class="param-name">Duration (weeks)</span><span class="param-val" id="vDur">20</span></div>
      <input type="range" id="duration" min="1" max="99" value="20">
    </div>

    <div class="sec" style="margin-top:2px">Turtle Shape</div>
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
      <div class="leg"><div class="leg-dot" style="background:#00cc44;box-shadow:0 0 6px #00cc44"></div>Healthy</div>
      <div class="leg"><div class="leg-dot" style="background:#ff3d5a;box-shadow:0 0 6px #ff3d5a"></div>Sick</div>
      <div class="leg"><div class="leg-dot" style="background:#8899bb;box-shadow:0 0 6px #8899bb"></div>Immune</div>
    </div>
  </div>

  <!-- RIGHT -->
  <div class="rp">
    <div class="sec">Live Stats</div>
    <div class="stats-row">
      <div class="stat">
        <div class="stat-lbl">% Infected</div>
        <div class="stat-val" id="sInf" style="color:#ff3d5a">0.0%</div>
        <div class="stat-bar"><div class="stat-bar-fill" id="bInf" style="background:#ff3d5a;width:0%"></div></div>
      </div>
      <div class="stat">
        <div class="stat-lbl">% Immune</div>
        <div class="stat-val" id="sImm" style="color:#8899bb">0.0%</div>
        <div class="stat-bar"><div class="stat-bar-fill" id="bImm" style="background:#8899bb;width:0%"></div></div>
      </div>
      <div class="stat">
        <div class="stat-lbl">Time (yrs)</div>
        <div class="stat-val" id="sTime" style="color:var(--accent)">0.00</div>
      </div>
    </div>

    <div class="graph-title">Population Graph</div>
    <canvas id="graphCanvas"></canvas>

    <div class="graph-key">
      <div class="gk"><div class="gk-line" style="background:#ff3d5a"></div>Sick</div>
      <div class="gk"><div class="gk-line" style="background:#8899bb"></div>Immune</div>
      <div class="gk"><div class="gk-line" style="background:#00cc44"></div>Healthy</div>
      <div class="gk"><div class="gk-line" style="background:#e0e8ff"></div>Total</div>
    </div>
  </div>

</div>

<script>
// ═══════════════════════════════════════════════════════════
// CONSTANTS — matching NetLogo source exactly
// ═══════════════════════════════════════════════════════════
const LIFESPAN          = 50 * 52;   // 2600 weeks
const CARRYING_CAPACITY = 300;
const CHANCE_REPRODUCE  = 1;         // 1% per tick
const IMMUNITY_DURATION = 52;        // weeks
const CONTACT_RADIUS    = 11;        // px — "same patch" equivalent
const CELL              = CONTACT_RADIUS * 2;
const MAX_HIST          = 400;
const INITIAL_SICK      = 10;        // NetLogo starts with 10 sick

// ═══════════════════════════════════════════════════════════
// CANVAS
// ═══════════════════════════════════════════════════════════
const SIM  = document.getElementById('simCanvas');
const GRP  = document.getElementById('graphCanvas');
const sCtx = SIM.getContext('2d');
const gCtx = GRP.getContext('2d');

function resize() {
  const area = document.querySelector('.sim-area');
  SIM.width  = area.clientWidth;
  SIM.height = area.clientHeight;
  GRP.width  = GRP.clientWidth;
  GRP.height = GRP.clientHeight;
}
window.addEventListener('resize', () => { resize(); drawGraph(); });
resize();

// ═══════════════════════════════════════════════════════════
// PARAMS
// ═══════════════════════════════════════════════════════════
const P = id => parseFloat(document.getElementById(id).value);

// ═══════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════
let agents = [], tick = 0, running = false, rafId = null;
let hist = { sick:[], immune:[], healthy:[], total:[] };
let agentShape = 'person';
let nextId = 0;

// ═══════════════════════════════════════════════════════════
// AGENT — mirrors NetLogo turtle properties
// ═══════════════════════════════════════════════════════════
class Agent {
  constructor(x, y, age, sick) {
    this.id   = nextId++;
    this.x    = x;
    this.y    = y;
    this.age  = age;
    this.angle = Math.random() * 360;  // degrees like NetLogo
    this.alive = true;

    // NetLogo fields
    this.sick_q             = false;
    this.sick_time          = 0;
    this.remaining_immunity = 0;

    if (sick) this.getSick();
  }

  // NetLogo: immune? reporter
  get immune() { return this.remaining_immunity > 0; }

  getSick()    { this.sick_q = true;  this.remaining_immunity = 0; }
  getHealthy() { this.sick_q = false; this.remaining_immunity = 0; this.sick_time = 0; }
  becomeImmune() {
    this.sick_q   = false;
    this.sick_time = 0;
    this.remaining_immunity = IMMUNITY_DURATION;
  }

  // NetLogo: get-older
  getOlder() {
    this.age++;
    if (this.age > LIFESPAN) { this.alive = false; return; }
    if (this.immune)   this.remaining_immunity--;
    if (this.sick_q)   this.sick_time++;
  }

  // NetLogo: move — rt random 100 / lt random 100 / fd 1
  move(W, H) {
    this.angle += Math.floor(Math.random() * 100) - Math.floor(Math.random() * 100);
    const rad = this.angle * Math.PI / 180;
    // fd 1 in patch units → scale to canvas (patches ~6px wide)
    const step = 6;
    this.x += Math.cos(rad) * step;
    this.y += Math.sin(rad) * step;
    // wrap
    if (this.x < 0)  this.x += W;
    if (this.x >= W) this.x -= W;
    if (this.y < 0)  this.y += H;
    if (this.y >= H) this.y -= H;
  }

  draw(ctx) {
    const col = this.sick_q  ? '#ff3d5a'
              : this.immune  ? '#8899bb'
              : '#00cc44';
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.fillStyle   = col;
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
      ctx.beginPath(); ctx.arc(0, 0, s*.75, 0, Math.PI*2); ctx.fill();
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

// ═══════════════════════════════════════════════════════════
// SPATIAL GRID — prevents O(n²) infection checks
// ═══════════════════════════════════════════════════════════
function buildGrid(W, H) {
  const cols = Math.ceil(W / CELL) + 1;
  const rows = Math.ceil(H / CELL) + 1;
  const grid = {};
  for (const a of agents) {
    const k = Math.floor(a.x / CELL) + ',' + Math.floor(a.y / CELL);
    if (!grid[k]) grid[k] = [];
    grid[k].push(a);
  }
  return { grid, cols, rows };
}

function nearby(grid, a) {
  const cx = Math.floor(a.x / CELL);
  const cy = Math.floor(a.y / CELL);
  const out = [];
  for (let dr = -1; dr <= 1; dr++)
    for (let dc = -1; dc <= 1; dc++) {
      const k = (cx+dc) + ',' + (cy+dr);
      if (grid[k]) for (const b of grid[k]) if (b !== a) out.push(b);
    }
  return out;
}

// ═══════════════════════════════════════════════════════════
// SETUP
// ═══════════════════════════════════════════════════════════
function setup() {
  if (running) stop();
  tick = 0; nextId = 0;
  hist = { sick:[], immune:[], healthy:[], total:[] };
  agents = [];

  const n = Math.round(P('population'));
  const W = SIM.width, H = SIM.height;

  // Create turtles — all healthy first
  for (let i = 0; i < n; i++) {
    const a = new Agent(
      16 + Math.random() * (W - 32),
      16 + Math.random() * (H - 32),
      Math.floor(Math.random() * LIFESPAN),
      false
    );
    agents.push(a);
  }

  // Infect 10 (or fewer if population < 10)
  const toInfect = Math.min(INITIAL_SICK, agents.length);
  const shuffled = [...agents].sort(() => Math.random() - 0.5);
  for (let i = 0; i < toInfect; i++) shuffled[i].getSick();

  drawSim(); drawGraph(); updateStats();
}

// ═══════════════════════════════════════════════════════════
// GO — one tick, faithful to NetLogo go procedure
// ═══════════════════════════════════════════════════════════
function doTick() {
  const infectiousness = P('infectiousness');
  const chanceRecover  = P('chanceRecover');
  const duration       = P('duration');
  const W = SIM.width, H = SIM.height;

  // Build spatial grid once
  const { grid } = buildGrid(W, H);

  const toAdd = [];  // new hatchlings

  for (const a of agents) {
    if (!a.alive) continue;

    // get-older
    a.getOlder();
    if (!a.alive) continue;

    // move
    a.move(W, H);

    if (a.sick_q) {
      // recover-or-die
      if (a.sick_time > duration) {
        if (Math.random() * 100 < chanceRecover) {
          a.becomeImmune();
        } else {
          a.alive = false;  // die
        }
      }

      if (a.alive && a.sick_q) {
        // infect — ask other turtles-here (nearby) with [not sick? and not immune?]
        const R2 = CONTACT_RADIUS * CONTACT_RADIUS;
        for (const b of nearby(grid, a)) {
          if (!b.alive || b.sick_q || b.immune) continue;
          const dx = a.x - b.x, dy = a.y - b.y;
          if (dx*dx + dy*dy < R2) {
            if (Math.random() * 100 < infectiousness) b.getSick();
          }
        }
      }
    } else {
      // reproduce — if not sick
      if (agents.length + toAdd.length < CARRYING_CAPACITY &&
          Math.random() * 100 < CHANCE_REPRODUCE) {
        const childAngle = (a.angle - 45) * Math.PI / 180;
        const cx = a.x + Math.cos(childAngle) * 6;
        const cy = a.y + Math.sin(childAngle) * 6;
        const child = new Agent(
          Math.max(0, Math.min(W, cx)),
          Math.max(0, Math.min(H, cy)),
          1, false
        );
        toAdd.push(child);
      }
    }
  }

  // Add newborns
  for (const c of toAdd) agents.push(c);

  // Remove dead
  agents = agents.filter(a => a.alive);

  tick++;

  // Record history every 4 ticks
  if (tick % 4 === 0) {
    const nSick   = agents.filter(a => a.sick_q).length;
    const nImmune = agents.filter(a => a.immune).length;
    const nHealth = agents.length - nSick - nImmune;
    hist.sick.push(nSick);
    hist.immune.push(nImmune);
    hist.healthy.push(nHealth);
    hist.total.push(agents.length);
    if (hist.sick.length > MAX_HIST) {
      hist.sick.shift(); hist.immune.shift();
      hist.healthy.shift(); hist.total.shift();
    }
  }
}

// ═══════════════════════════════════════════════════════════
// RENDER
// ═══════════════════════════════════════════════════════════
function drawSim() {
  sCtx.fillStyle = '#070d1a';
  sCtx.fillRect(0, 0, SIM.width, SIM.height);
  for (const a of agents) a.draw(sCtx);
}

function drawGraph() {
  const W = GRP.width, H = GRP.height;
  gCtx.fillStyle = '#101c30';
  gCtx.fillRect(0, 0, W, H);

  const n = hist.sick.length;
  if (n < 2) return;

  const pad  = { t:12, b:28, l:36, r:10 };
  const gW   = W - pad.l - pad.r;
  const gH   = H - pad.t - pad.b;
  const maxY = CARRYING_CAPACITY;

  // Y grid + labels
  gCtx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + (i/4)*gH;
    gCtx.strokeStyle = 'rgba(26,46,74,.9)';
    gCtx.beginPath(); gCtx.moveTo(pad.l,y); gCtx.lineTo(W-pad.r,y); gCtx.stroke();
    gCtx.fillStyle = 'rgba(61,80,112,.95)';
    gCtx.font = '9px Share Tech Mono';
    gCtx.textAlign = 'right';
    gCtx.fillText(Math.round(maxY*(1-i/4)), pad.l-4, y+3);
  }

  // X labels (years)
  gCtx.fillStyle = 'rgba(61,80,112,.8)';
  gCtx.font = '8px Share Tech Mono';
  gCtx.textAlign = 'center';
  for (let i = 0; i <= 4; i++) {
    const x = pad.l + (i/4)*gW;
    const yr = (i/4 * n * 4 / 52).toFixed(1);
    gCtx.fillText(yr+'y', x, H - pad.b + 14);
  }

  function line(arr, color, lw) {
    if (arr.length < 2) return;
    gCtx.beginPath();
    gCtx.strokeStyle = color;
    gCtx.lineWidth   = lw;
    gCtx.shadowColor = color;
    gCtx.shadowBlur  = 4;
    gCtx.lineJoin    = 'round';
    arr.forEach((v, i) => {
      const x = pad.l + (i/(arr.length-1))*gW;
      const y = pad.t + gH - Math.min(v/maxY, 1)*gH;
      i===0 ? gCtx.moveTo(x,y) : gCtx.lineTo(x,y);
    });
    gCtx.stroke();
    gCtx.shadowBlur = 0;
  }

  line(hist.total,   '#e0e8ff', 1.5);
  line(hist.healthy, '#00cc44', 2);
  line(hist.immune,  '#8899bb', 2);
  line(hist.sick,    '#ff3d5a', 2.5);
}

function updateStats() {
  const total  = agents.length || 1;
  const nSick  = agents.filter(a => a.sick_q).length;
  const nImm   = agents.filter(a => a.immune).length;
  const pI = (nSick/total*100).toFixed(1);
  const pM = (nImm /total*100).toFixed(1);
  document.getElementById('sInf').textContent  = pI + '%';
  document.getElementById('sImm').textContent  = pM + '%';
  document.getElementById('sTime').textContent = (tick/52).toFixed(2);
  document.getElementById('bInf').style.width  = pI + '%';
  document.getElementById('bImm').style.width  = pM + '%';
}

// ═══════════════════════════════════════════════════════════
// LOOP — speed slider = frames per second (3–30)
// ═══════════════════════════════════════════════════════════
function loop() {
  if (!running) return;
  doTick();
  drawSim();
  drawGraph();
  updateStats();
  const fps = P('speed') * 3;
  rafId = setTimeout(() => requestAnimationFrame(loop), 1000 / fps);
}

function start() {
  if (running) return;
  if (agents.length === 0) setup();
  running = true;
  document.getElementById('btnGo').textContent = '⏸  PAUSE';
  document.getElementById('btnGo').classList.add('on');
  requestAnimationFrame(loop);
}

function stop() {
  running = false;
  clearTimeout(rafId);
  document.getElementById('btnGo').textContent = '▶  GO';
  document.getElementById('btnGo').classList.remove('on');
}

document.getElementById('btnGo').addEventListener('click', () => {
  running ? stop() : start();
});
document.getElementById('btnSetup').addEventListener('click', setup);

// ─── Sliders ───
function bindSlider(id, valId, suffix) {
  const el = document.getElementById(id);
  const vl = document.getElementById(valId);
  function u() {
    vl.textContent = el.value + (suffix||'');
    el.style.setProperty('--pct', ((el.value-el.min)/(el.max-el.min)*100)+'%');
  }
  el.addEventListener('input', u); u();
}
bindSlider('speed',          'vSpd', '');
bindSlider('population',     'vPop', '');
bindSlider('infectiousness', 'vInf', '%');
bindSlider('chanceRecover',  'vRec', '%');
bindSlider('duration',       'vDur', '');

// ─── Shapes ───
document.querySelectorAll('.shape-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.shape-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    agentShape = btn.dataset.shape;
  });
});

setup();
</script>
</body>
</html>"""

components.html(HTML, height=860, scrolling=False)
