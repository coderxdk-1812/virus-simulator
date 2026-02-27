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
    --bg:#070d1a; --panel:#0c1425; --card:#0e1828; --border:#1a2e4a;
    --accent:#00d4ff; --sick:#ff3d5a; --immune:#7a8faa; --healthy:#00cc44;
    --total:#c8d8f0; --text:#b8cce8; --dim:#3d5070;
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
    background:var(--healthy); box-shadow:0 0 8px var(--healthy);
    animation:blink 2s infinite; flex-shrink:0;
  }
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
  .h-title { font-family:var(--mono); font-size:15px; color:var(--accent); letter-spacing:3px; }
  .h-sub   { font-size:11px; color:var(--dim); letter-spacing:2px; margin-left:auto; }

  /* LAYOUT */
  .layout { display:flex; flex:1; overflow:hidden; }

  /* LEFT CONTROLS */
  .lp {
    width:248px; min-width:248px;
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
    display:flex; gap:18px; background:rgba(7,13,26,.92);
    border:1px solid var(--border); border-radius:7px; padding:7px 20px; z-index:2;
  }
  .leg     { display:flex; align-items:center; gap:7px; font-size:12px; font-weight:700; }
  .leg-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }

  /* RIGHT PANEL */
  .rp {
    width:380px; min-width:380px;
    background:var(--panel); border-left:1px solid var(--border);
    display:flex; flex-direction:column; padding:14px 16px; gap:10px; overflow:hidden;
  }

  /* 3 stat cards */
  .stats-row { display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; flex-shrink:0; }
  .stat { background:var(--card); border:1px solid var(--border); border-radius:7px; padding:10px 10px 8px; }
  .stat-lbl { font-family:var(--mono); font-size:8px; color:var(--dim); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:3px; }
  .stat-val { font-family:var(--mono); font-size:20px; font-weight:700; line-height:1; }
  .stat-bar { height:3px; background:var(--border); border-radius:2px; overflow:hidden; margin-top:6px; }
  .stat-bar-fill { height:100%; border-radius:2px; transition:width .4s; }

  /* Graph section — square canvas */
  .graph-header {
    font-family:var(--mono); font-size:10px; color:var(--accent);
    letter-spacing:2px; text-transform:uppercase;
    border-bottom:1px solid var(--border); padding-bottom:5px; flex-shrink:0;
  }
  .graph-wrap {
    flex:1;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    min-height:0;
  }
  /* Square canvas: use aspect-ratio trick */
  .graph-canvas-box {
    position:relative;
    width:100%;
    /* square: height = width via padding trick */
    aspect-ratio:1/1;
    max-height:100%;
    flex-shrink:1;
  }
  #graphCanvas {
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    border:1px solid var(--border);
    border-radius:7px;
    background:var(--card);
  }

  /* Graph key */
  .graph-key { display:grid; grid-template-columns:1fr 1fr; gap:5px 16px; flex-shrink:0; padding-top:2px; }
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

  <!-- LEFT -->
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
      <div class="param-top"><span class="param-name">Initial Infected</span><span class="param-val" id="vSick">10</span></div>
      <input type="range" id="initialSick" min="1" max="50" value="10">
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
      <div class="leg"><div class="leg-dot" style="background:#7a8faa;box-shadow:0 0 4px #7a8faa"></div>Immune</div>
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
        <div class="stat-val" id="sImm" style="color:#7a8faa">0.0%</div>
        <div class="stat-bar"><div class="stat-bar-fill" id="bImm" style="background:#7a8faa;width:0%"></div></div>
      </div>
      <div class="stat">
        <div class="stat-lbl">Time (yrs)</div>
        <div class="stat-val" id="sTime" style="color:var(--accent)">0.00</div>
      </div>
    </div>

    <div class="graph-header">Population Graph</div>

    <div class="graph-wrap">
      <div class="graph-canvas-box">
        <canvas id="graphCanvas"></canvas>
      </div>
    </div>

    <div class="graph-key">
      <div class="gk"><div class="gk-line" style="background:#ff3d5a"></div>Sick (I)</div>
      <div class="gk"><div class="gk-line" style="background:#7a8faa"></div>Immune (R)</div>
      <div class="gk"><div class="gk-line" style="background:#00cc44"></div>Healthy (S)</div>
      <div class="gk"><div class="gk-line" style="background:#c8d8f0"></div>Total</div>
    </div>
  </div>

</div>

<script>
// ═══════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════
const LIFESPAN          = 50 * 52;
const CARRYING_CAPACITY = 300;
const CHANCE_REPRODUCE  = 1;
const IMMUNITY_DURATION = 52;
const CONTACT_RADIUS    = 11;
const CELL              = CONTACT_RADIUS * 2;
const MAX_HIST          = 400;

// ═══════════════════════════════════════════════════════════
// CANVAS REFS
// ═══════════════════════════════════════════════════════════
const SIM  = document.getElementById('simCanvas');
const GRP  = document.getElementById('graphCanvas');
const sCtx = SIM.getContext('2d');
const gCtx = GRP.getContext('2d');

function resizeSim() {
  const area = document.querySelector('.sim-area');
  SIM.width  = area.clientWidth;
  SIM.height = area.clientHeight;
}
function resizeGraph() {
  const box  = document.querySelector('.graph-canvas-box');
  const size = box.clientWidth;   // square — width = height
  GRP.width  = size;
  GRP.height = size;
}
function resizeAll() { resizeSim(); resizeGraph(); drawGraph(); }
window.addEventListener('resize', resizeAll);
resizeSim();
// graph resize after layout paint
requestAnimationFrame(() => { resizeGraph(); drawGraph(); });

// ═══════════════════════════════════════════════════════════
// PARAMS
// ═══════════════════════════════════════════════════════════
const P = id => parseFloat(document.getElementById(id).value);

// ═══════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════
let agents = [], tick = 0, running = false, rafId = null, nextId = 0;
let hist = { sick:[], immune:[], healthy:[], total:[] };
let agentShape = 'person';

// ═══════════════════════════════════════════════════════════
// AGENT
// ═══════════════════════════════════════════════════════════
class Agent {
  constructor(x, y, age, sick) {
    this.id    = nextId++;
    this.x     = x; this.y = y;
    this.age   = age;
    this.angle = Math.random() * 360;
    this.alive = true;
    this.sick_q             = false;
    this.sick_time          = 0;
    this.remaining_immunity = 0;
    if (sick) this.getSick();
  }
  get immune() { return this.remaining_immunity > 0; }
  getSick()    { this.sick_q = true;  this.remaining_immunity = 0; }
  getHealthy() { this.sick_q = false; this.remaining_immunity = 0; this.sick_time = 0; }
  becomeImmune() { this.sick_q = false; this.sick_time = 0; this.remaining_immunity = IMMUNITY_DURATION; }

  getOlder() {
    this.age++;
    if (this.age > LIFESPAN) { this.alive = false; return; }
    if (this.immune)  this.remaining_immunity--;
    if (this.sick_q)  this.sick_time++;
  }

  move(W, H) {
    this.angle += Math.floor(Math.random()*100) - Math.floor(Math.random()*100);
    const rad = this.angle * Math.PI / 180;
    this.x += Math.cos(rad) * 6;
    this.y += Math.sin(rad) * 6;
    if (this.x < 0)  this.x += W;
    if (this.x >= W) this.x -= W;
    if (this.y < 0)  this.y += H;
    if (this.y >= H) this.y -= H;
  }

  draw(ctx) {
    const col = this.sick_q ? '#ff3d5a' : this.immune ? '#7a8faa' : '#00cc44';
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.fillStyle = col; ctx.strokeStyle = col;
    ctx.shadowColor = col; ctx.shadowBlur = 6;
    const s = 6;
    if (agentShape === 'person') {
      ctx.beginPath(); ctx.arc(0,-s*1.55,s*.62,0,Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.rect(-s*.42,-s*.88,s*.84,s*1.3); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(-s*.22,s*.42); ctx.lineTo(-s*.48,s*1.4);
      ctx.moveTo( s*.22,s*.42); ctx.lineTo( s*.48,s*1.4);
      ctx.lineWidth=s*.42; ctx.lineCap='round'; ctx.stroke();
    } else if (agentShape === 'circle') {
      ctx.beginPath(); ctx.arc(0,0,s*.75,0,Math.PI*2); ctx.fill();
    } else if (agentShape === 'triangle') {
      ctx.beginPath(); ctx.moveTo(0,-s); ctx.lineTo(s*.87,s*.5); ctx.lineTo(-s*.87,s*.5); ctx.closePath(); ctx.fill();
    } else {
      ctx.beginPath(); ctx.moveTo(0,-s*.95); ctx.lineTo(s*.6,0); ctx.lineTo(0,s*.95); ctx.lineTo(-s*.6,0); ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  }
}

// ═══════════════════════════════════════════════════════════
// SPATIAL GRID
// ═══════════════════════════════════════════════════════════
function nearby(a) {
  const cx = Math.floor(a.x/CELL), cy = Math.floor(a.y/CELL);
  const out = [];
  for (let dr=-1;dr<=1;dr++) for (let dc=-1;dc<=1;dc++) {
    const k=(cx+dc)+','+(cy+dr);
    if (_grid[k]) for (const b of _grid[k]) if (b!==a) out.push(b);
  }
  return out;
}
let _grid = {};
function buildGrid() {
  _grid = {};
  for (const a of agents) {
    const k=Math.floor(a.x/CELL)+','+Math.floor(a.y/CELL);
    if (!_grid[k]) _grid[k]=[];
    _grid[k].push(a);
  }
}

// ═══════════════════════════════════════════════════════════
// SETUP
// ═══════════════════════════════════════════════════════════
function setup() {
  if (running) stop();
  tick=0; nextId=0;
  hist={sick:[],immune:[],healthy:[],total:[]};
  agents=[];
  const n   = Math.round(P('population'));
  const ns  = Math.min(Math.round(P('initialSick')), n);
  const W   = SIM.width, H = SIM.height;
  for (let i=0;i<n;i++) {
    agents.push(new Agent(
      16+Math.random()*(W-32),
      16+Math.random()*(H-32),
      Math.floor(Math.random()*LIFESPAN), false
    ));
  }
  // infect first ns agents (shuffled)
  agents.sort(()=>Math.random()-.5);
  for (let i=0;i<ns;i++) agents[i].getSick();
  drawSim(); resizeGraph(); drawGraph(); updateStats();
}

// ═══════════════════════════════════════════════════════════
// TICK
// ═══════════════════════════════════════════════════════════
function doTick() {
  const infectP = P('infectiousness');
  const recoverP= P('chanceRecover');
  const dur     = P('duration');
  const W=SIM.width, H=SIM.height;
  const R2=CONTACT_RADIUS*CONTACT_RADIUS;

  buildGrid();
  const toAdd=[];

  for (const a of agents) {
    if (!a.alive) continue;
    a.getOlder();
    if (!a.alive) continue;
    a.move(W,H);

    if (a.sick_q) {
      if (a.sick_time > dur) {
        if (Math.random()*100 < recoverP) a.becomeImmune();
        else a.alive=false;
      }
      if (a.alive && a.sick_q) {
        for (const b of nearby(a)) {
          if (!b.alive||b.sick_q||b.immune) continue;
          const dx=a.x-b.x, dy=a.y-b.y;
          if (dx*dx+dy*dy<R2 && Math.random()*100<infectP) b.getSick();
        }
      }
    } else {
      if (agents.length+toAdd.length<CARRYING_CAPACITY && Math.random()*100<CHANCE_REPRODUCE) {
        const ca=(a.angle-45)*Math.PI/180;
        toAdd.push(new Agent(
          Math.max(0,Math.min(W, a.x+Math.cos(ca)*6)),
          Math.max(0,Math.min(H, a.y+Math.sin(ca)*6)),
          1, false
        ));
      }
    }
  }

  for (const c of toAdd) agents.push(c);
  agents=agents.filter(a=>a.alive);
  tick++;

  if (tick%4===0) {
    const nS=agents.filter(a=>a.sick_q).length;
    const nI=agents.filter(a=>a.immune).length;
    hist.sick.push(nS); hist.immune.push(nI);
    hist.healthy.push(agents.length-nS-nI); hist.total.push(agents.length);
    if (hist.sick.length>MAX_HIST) { hist.sick.shift();hist.immune.shift();hist.healthy.shift();hist.total.shift(); }
  }
}

// ═══════════════════════════════════════════════════════════
// DRAW SIM
// ═══════════════════════════════════════════════════════════
function drawSim() {
  sCtx.fillStyle='#070d1a';
  sCtx.fillRect(0,0,SIM.width,SIM.height);
  for (const a of agents) a.draw(sCtx);
}

// ═══════════════════════════════════════════════════════════
// DRAW GRAPH — square with full axes
// ═══════════════════════════════════════════════════════════
function drawGraph() {
  const W=GRP.width, H=GRP.height;
  if (W===0||H===0) return;

  gCtx.fillStyle='#0e1828';
  gCtx.fillRect(0,0,W,H);

  // Padding — extra on left & bottom for axis labels
  const pad = { t:14, b:42, l:46, r:14 };
  const gW  = W - pad.l - pad.r;
  const gH  = H - pad.t - pad.b;
  const maxY= CARRYING_CAPACITY;
  const n   = hist.sick.length;

  // ── Axis lines ──
  gCtx.strokeStyle='rgba(40,65,100,.9)';
  gCtx.lineWidth=1;
  // Y axis
  gCtx.beginPath(); gCtx.moveTo(pad.l,pad.t); gCtx.lineTo(pad.l,pad.t+gH); gCtx.stroke();
  // X axis
  gCtx.beginPath(); gCtx.moveTo(pad.l,pad.t+gH); gCtx.lineTo(pad.l+gW,pad.t+gH); gCtx.stroke();

  // ── Y grid lines + labels ──
  const ySteps = 5;
  for (let i=0;i<=ySteps;i++) {
    const y   = pad.t + (i/ySteps)*gH;
    const val = Math.round(maxY*(1-i/ySteps));

    // grid line
    gCtx.strokeStyle='rgba(26,46,74,.6)';
    gCtx.lineWidth=0.5;
    gCtx.setLineDash([3,4]);
    gCtx.beginPath(); gCtx.moveTo(pad.l+1,y); gCtx.lineTo(pad.l+gW,y); gCtx.stroke();
    gCtx.setLineDash([]);

    // tick mark
    gCtx.strokeStyle='rgba(40,65,100,.9)';
    gCtx.lineWidth=1;
    gCtx.beginPath(); gCtx.moveTo(pad.l-4,y); gCtx.lineTo(pad.l,y); gCtx.stroke();

    // label
    gCtx.fillStyle='rgba(100,140,180,.9)';
    gCtx.font='bold 9px Share Tech Mono';
    gCtx.textAlign='right';
    gCtx.fillText(val, pad.l-7, y+3);
  }

  // Y axis title
  gCtx.save();
  gCtx.translate(11, pad.t + gH/2);
  gCtx.rotate(-Math.PI/2);
  gCtx.fillStyle='rgba(80,120,160,.8)';
  gCtx.font='9px Share Tech Mono';
  gCtx.textAlign='center';
  gCtx.fillText('POPULATION', 0, 0);
  gCtx.restore();

  // ── X grid lines + labels (time in years) ──
  const xSteps = 5;
  for (let i=0;i<=xSteps;i++) {
    const x = pad.l + (i/xSteps)*gW;

    // grid line (skip x=0 since that's the axis)
    if (i>0) {
      gCtx.strokeStyle='rgba(26,46,74,.6)';
      gCtx.lineWidth=0.5;
      gCtx.setLineDash([3,4]);
      gCtx.beginPath(); gCtx.moveTo(x,pad.t); gCtx.lineTo(x,pad.t+gH-1); gCtx.stroke();
      gCtx.setLineDash([]);
    }

    // tick mark
    gCtx.strokeStyle='rgba(40,65,100,.9)';
    gCtx.lineWidth=1;
    gCtx.beginPath(); gCtx.moveTo(x,pad.t+gH); gCtx.lineTo(x,pad.t+gH+4); gCtx.stroke();

    // label — years elapsed at this x position
    const yr = n>1 ? (i/xSteps * n * 4 / 52).toFixed(1) : '0.0';
    gCtx.fillStyle='rgba(100,140,180,.9)';
    gCtx.font='bold 9px Share Tech Mono';
    gCtx.textAlign='center';
    gCtx.fillText(yr+'y', x, pad.t+gH+15);
  }

  // X axis title
  gCtx.fillStyle='rgba(80,120,160,.8)';
  gCtx.font='9px Share Tech Mono';
  gCtx.textAlign='center';
  gCtx.fillText('TIME (YEARS)', pad.l+gW/2, H-4);

  // ── Plot lines ──
  if (n < 2) return;

  function plotLine(arr, color, lw) {
    if (arr.length<2) return;
    gCtx.beginPath();
    gCtx.strokeStyle=color;
    gCtx.lineWidth=lw;
    gCtx.shadowColor=color;
    gCtx.shadowBlur=4;
    gCtx.lineJoin='round';
    gCtx.lineCap='round';
    arr.forEach((v,i)=>{
      const x=pad.l+(i/(arr.length-1))*gW;
      const y=pad.t+gH-Math.min(v/maxY,1)*gH;
      i===0?gCtx.moveTo(x,y):gCtx.lineTo(x,y);
    });
    gCtx.stroke();
    gCtx.shadowBlur=0;
  }

  plotLine(hist.total,   '#c8d8f0', 1.5);
  plotLine(hist.healthy, '#00cc44', 2);
  plotLine(hist.immune,  '#7a8faa', 2);
  plotLine(hist.sick,    '#ff3d5a', 2.5);
}

// ═══════════════════════════════════════════════════════════
// STATS
// ═══════════════════════════════════════════════════════════
function updateStats() {
  const total=agents.length||1;
  const nS=agents.filter(a=>a.sick_q).length;
  const nI=agents.filter(a=>a.immune).length;
  const pI=(nS/total*100).toFixed(1), pM=(nI/total*100).toFixed(1);
  document.getElementById('sInf').textContent =pI+'%';
  document.getElementById('sImm').textContent =pM+'%';
  document.getElementById('sTime').textContent=(tick/52).toFixed(2);
  document.getElementById('bInf').style.width =pI+'%';
  document.getElementById('bImm').style.width =pM+'%';
}

// ═══════════════════════════════════════════════════════════
// LOOP
// ═══════════════════════════════════════════════════════════
function loop() {
  if (!running) return;
  doTick();
  drawSim();
  drawGraph();
  updateStats();
  rafId=setTimeout(()=>requestAnimationFrame(loop), 1000/(P('speed')*3));
}
function start() {
  if (running) return;
  if (agents.length===0) setup();
  running=true;
  document.getElementById('btnGo').textContent='⏸  PAUSE';
  document.getElementById('btnGo').classList.add('on');
  requestAnimationFrame(loop);
}
function stop() {
  running=false; clearTimeout(rafId);
  document.getElementById('btnGo').textContent='▶  GO';
  document.getElementById('btnGo').classList.remove('on');
}

document.getElementById('btnGo').addEventListener('click',()=>running?stop():start());
document.getElementById('btnSetup').addEventListener('click',setup);

// ═══════════════════════════════════════════════════════════
// SLIDERS
// ═══════════════════════════════════════════════════════════
function bindSlider(id,valId,suffix) {
  const el=document.getElementById(id), vl=document.getElementById(valId);
  function u(){
    vl.textContent=el.value+(suffix||'');
    el.style.setProperty('--pct',((el.value-el.min)/(el.max-el.min)*100)+'%');
  }
  el.addEventListener('input',u); u();
}
bindSlider('speed',         'vSpd','');
bindSlider('population',    'vPop','');
bindSlider('initialSick',   'vSick','');
bindSlider('infectiousness','vInf','%');
bindSlider('chanceRecover', 'vRec','%');
bindSlider('duration',      'vDur','');

// clamp initialSick max to population
document.getElementById('population').addEventListener('input',()=>{
  const maxSick=document.getElementById('population');
  const sickEl =document.getElementById('initialSick');
  if (parseInt(sickEl.value)>parseInt(maxSick.value)) {
    sickEl.value=maxSick.value;
    sickEl.dispatchEvent(new Event('input'));
  }
  sickEl.max=maxSick.value;
});

// ═══════════════════════════════════════════════════════════
// SHAPES
// ═══════════════════════════════════════════════════════════
document.querySelectorAll('.shape-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.shape-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active'); agentShape=btn.dataset.shape;
  });
});

setup();
</script>
</body>
</html>"""

components.html(HTML, height=860, scrolling=False)
