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
    .stApp { background: #080c18; }
</style>
""", unsafe_allow_html=True)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  :root{
    --bg:#080c18;--panel:#0d1326;--panel2:#111827;--border:#1e2d4a;
    --accent:#00d4ff;--sick:#ff3d5a;--immune:#00e5a0;--healthy:#4a9eff;
    --total:#f0f0f0;--text:#c8d8f0;--dim:#4a5568;
  }
  body{font-family:'Rajdhani',sans-serif;background:var(--bg);color:var(--text);
    height:860px;overflow:hidden;display:flex;flex-direction:column}

  /* HEADER */
  .hdr{background:var(--panel);border-bottom:1px solid var(--border);
    padding:8px 24px;display:flex;align-items:center;gap:14px;flex-shrink:0}
  .hdr-title{font-family:'Share Tech Mono',monospace;font-size:16px;
    color:var(--accent);letter-spacing:3px}
  .hdr-sub{font-size:12px;color:var(--dim);letter-spacing:2px;margin-left:auto}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--immune);
    box-shadow:0 0 8px var(--immune);animation:pulse 2s infinite;flex-shrink:0}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

  .main{display:flex;flex:1;overflow:hidden}

  /* LEFT PANEL */
  .lp{width:260px;min-width:260px;background:var(--panel);
    border-right:1px solid var(--border);display:flex;flex-direction:column;
    padding:16px 18px;gap:12px;overflow-y:auto}

  .stitle{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--accent);
    letter-spacing:2px;text-transform:uppercase;border-bottom:1px solid var(--border);
    padding-bottom:5px;margin-bottom:4px}

  /* Slider control: label row on top, slider below full-width */
  .ctrl{display:flex;flex-direction:column;gap:5px}
  .ctrl-header{display:flex;justify-content:space-between;align-items:baseline;width:100%}
  .ctrl-label{font-size:14px;font-weight:600;color:var(--text);letter-spacing:0.3px}
  .cv{font-family:'Share Tech Mono',monospace;font-size:14px;color:var(--accent);
    white-space:nowrap;padding-left:8px}

  input[type=range]{
    -webkit-appearance:none;
    display:block;
    width:100%;
    height:5px;
    border-radius:3px;
    background:var(--border);
    outline:none;
    cursor:pointer;
    margin:0;
    padding:0;
  }
  input[type=range]::-webkit-slider-thumb{
    -webkit-appearance:none;
    width:16px;height:16px;
    border-radius:50%;
    background:var(--accent);
    box-shadow:0 0 7px var(--accent);
    cursor:pointer;
  }
  input[type=range]::-webkit-slider-runnable-track{
    background:linear-gradient(to right,var(--accent) 0%,var(--accent) var(--p,0%),var(--border) var(--p,0%));
    border-radius:3px;height:5px;
  }

  /* Shape buttons */
  .sgrid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
  .sbtn{padding:8px 4px;border:1px solid var(--border);border-radius:5px;
    background:var(--panel2);color:var(--dim);font-size:18px;cursor:pointer;
    text-align:center;transition:all .15s;line-height:1}
  .sbtn:hover{border-color:var(--accent);color:var(--accent)}
  .sbtn.active{border-color:var(--accent);background:rgba(0,212,255,.12);
    color:var(--accent);box-shadow:0 0 8px rgba(0,212,255,.25)}

  .spacer{flex:1;min-height:8px}
  .setup-btn{padding:10px;border:1px solid var(--border);border-radius:6px;
    background:var(--panel2);color:var(--dim);font-family:'Share Tech Mono',monospace;
    font-size:12px;letter-spacing:2px;cursor:pointer;transition:all .2s;width:100%}
  .setup-btn:hover{border-color:var(--accent);color:var(--text)}
  .go-btn{padding:13px;border:2px solid var(--accent);border-radius:7px;
    background:rgba(0,212,255,.08);color:var(--accent);width:100%;
    font-family:'Share Tech Mono',monospace;font-size:16px;letter-spacing:5px;
    cursor:pointer;transition:all .2s;box-shadow:0 0 12px rgba(0,212,255,.25)}
  .go-btn:hover{background:rgba(0,212,255,.2);box-shadow:0 0 22px rgba(0,212,255,.5)}
  .go-btn.running{border-color:var(--sick);color:var(--sick);
    background:rgba(255,61,90,.08);box-shadow:0 0 12px rgba(255,61,90,.3)}

  /* CENTER */
  .center{flex:1;display:flex;flex-direction:column;position:relative;overflow:hidden}
  .cwrap{position:relative;flex:1;overflow:hidden}
  .cwrap::before{content:'';position:absolute;inset:0;
    background-image:linear-gradient(rgba(30,45,74,.15) 1px,transparent 1px),
      linear-gradient(90deg,rgba(30,45,74,.15) 1px,transparent 1px);
    background-size:40px 40px;pointer-events:none;z-index:1}
  #simCanvas{width:100%;height:100%;display:block}
  .legend{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);
    display:flex;gap:20px;background:rgba(8,12,24,.9);border:1px solid var(--border);
    border-radius:7px;padding:8px 20px;z-index:2}
  .li{display:flex;align-items:center;gap:7px;font-size:13px;letter-spacing:1px;font-weight:600}
  .ld{width:10px;height:10px;border-radius:50%;flex-shrink:0}

  /* RIGHT PANEL */
  .rp{width:270px;min-width:270px;background:var(--panel);
    border-left:1px solid var(--border);display:flex;flex-direction:column;
    padding:16px 18px;gap:10px;overflow:hidden}

  .sc{background:var(--panel2);border:1px solid var(--border);border-radius:7px;padding:11px 14px}
  .sl{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--dim);
    letter-spacing:2px;text-transform:uppercase;margin-bottom:3px}
  .sv{font-family:'Share Tech Mono',monospace;font-size:26px;font-weight:700;line-height:1.1}
  .sbar{height:4px;border-radius:2px;background:var(--border);overflow:hidden;margin-top:6px}
  .sbf{height:100%;border-radius:2px;transition:width .3s}

  #graphCanvas{flex:1;width:100%;border:1px solid var(--border);
    border-radius:7px;background:var(--panel2);display:block}

  .gl{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;flex-shrink:0}
  .gli{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:var(--text)}
  .gll{width:18px;height:2px;border-radius:1px;flex-shrink:0}
</style>
</head>
<body>

<div class="hdr">
  <div class="dot"></div>
  <div class="hdr-title">VIRUSIM // Biological Spread Model</div>
  <div class="hdr-sub">NetLogo Virus Biology — Interactive</div>
</div>

<div class="main">
  <!-- LEFT PANEL -->
  <div class="lp">
    <div class="stitle">Parameters</div>

    <div class="ctrl">
      <div class="ctrl-header">
        <span class="ctrl-label">Model Speed</span>
        <span class="cv" id="vSpd">5</span>
      </div>
      <input type="range" id="speed" min="1" max="10" value="5">
    </div>

    <div class="ctrl">
      <div class="ctrl-header">
        <span class="ctrl-label">Population</span>
        <span class="cv" id="vPop">150</span>
      </div>
      <input type="range" id="population" min="10" max="500" value="150" step="5">
    </div>

    <div class="ctrl">
      <div class="ctrl-header">
        <span class="ctrl-label">Infectiousness</span>
        <span class="cv" id="vInf">65%</span>
      </div>
      <input type="range" id="infectiousness" min="0" max="100" value="65">
    </div>

    <div class="ctrl">
      <div class="ctrl-header">
        <span class="ctrl-label">Chance Recover</span>
        <span class="cv" id="vRec">25%</span>
      </div>
      <input type="range" id="chanceRecover" min="0" max="100" value="25">
    </div>

    <div class="ctrl">
      <div class="ctrl-header">
        <span class="ctrl-label">Duration (wks)</span>
        <span class="cv" id="vDur">20</span>
      </div>
      <input type="range" id="duration" min="1" max="100" value="20">
    </div>

    <div class="stitle" style="margin-top:4px">Agent Shape</div>
    <div class="sgrid">
      <button class="sbtn active" data-shape="person">🧍</button>
      <button class="sbtn" data-shape="circle">⬤</button>
      <button class="sbtn" data-shape="triangle">▲</button>
      <button class="sbtn" data-shape="diamond">◆</button>
    </div>

    <div class="spacer"></div>
    <button class="setup-btn" id="setupBtn">[ SETUP ]</button>
    <button class="go-btn" id="goBtn">▶  GO</button>
  </div>

  <!-- CENTER -->
  <div class="center">
    <div class="cwrap">
      <canvas id="simCanvas"></canvas>
      <div class="legend">
        <div class="li"><div class="ld" style="background:var(--healthy);box-shadow:0 0 6px var(--healthy)"></div>Susceptible</div>
        <div class="li"><div class="ld" style="background:var(--sick);box-shadow:0 0 6px var(--sick)"></div>Infected</div>
        <div class="li"><div class="ld" style="background:var(--immune);box-shadow:0 0 6px var(--immune)"></div>Recovered</div>
      </div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="rp">
    <div class="stitle">Live Stats</div>

    <div class="sc">
      <div class="sl">% Infected</div>
      <div class="sv" id="sInf" style="color:var(--sick)">0.0%</div>
      <div class="sbar"><div class="sbf" id="bInf" style="width:0%;background:var(--sick)"></div></div>
    </div>
    <div class="sc">
      <div class="sl">% Immune</div>
      <div class="sv" id="sImm" style="color:var(--immune)">0.0%</div>
      <div class="sbar"><div class="sbf" id="bImm" style="width:0%;background:var(--immune)"></div></div>
    </div>
    <div class="sc">
      <div class="sl">Elapsed Time</div>
      <div class="sv" id="sTime" style="color:var(--accent)">0.00 yrs</div>
    </div>

    <div class="stitle" style="margin-top:2px">Population Graph</div>
    <canvas id="graphCanvas"></canvas>

    <div class="gl">
      <div class="gli"><div class="gll" style="background:var(--sick)"></div>Sick</div>
      <div class="gli"><div class="gll" style="background:var(--immune)"></div>Immune</div>
      <div class="gli"><div class="gll" style="background:var(--healthy)"></div>Healthy</div>
      <div class="gli"><div class="gll" style="background:var(--total)"></div>Total</div>
    </div>
  </div>
</div>

<script>
const COL={sick:'#ff3d5a',immune:'#00e5a0',healthy:'#4a9eff',total:'#f0f0f0',bg:'#080c18',panel2:'#111827',border:'#1e2d4a'};
const sc=document.getElementById('simCanvas').getContext('2d');
const gc=document.getElementById('graphCanvas').getContext('2d');
const SIM=document.getElementById('simCanvas');
const GRP=document.getElementById('graphCanvas');

let agents=[],running=false,animId=null,tick=0,lastTs=0,accum=0;
let gd={sick:[],immune:[],healthy:[],total:[]};
let shape='person';

const gv=id=>parseFloat(document.getElementById(id).value);

function resize(){
  const w=document.querySelector('.cwrap');
  SIM.width=w.clientWidth; SIM.height=w.clientHeight;
  GRP.width=GRP.clientWidth; GRP.height=GRP.clientHeight;
}
window.addEventListener('resize',()=>{resize();drawGraph();});
resize();

class Agent{
  constructor(x,y,st){
    this.x=x;this.y=y;this.state=st;
    this.angle=Math.random()*Math.PI*2;
    this.spd=1.1+Math.random()*.9;
    this.infTick=st==='sick'?0:-1;
  }
  move(W,H){
    this.angle+=(Math.random()-.5)*.75;
    this.x+=Math.cos(this.angle)*this.spd;
    this.y+=Math.sin(this.angle)*this.spd;
    if(this.x<0)this.x+=W;if(this.x>W)this.x-=W;
    if(this.y<0)this.y+=H;if(this.y>H)this.y-=H;
  }
  draw(ctx){
    const col=this.state==='sick'?COL.sick:this.state==='immune'?COL.immune:COL.healthy;
    ctx.save();ctx.translate(this.x,this.y);
    ctx.fillStyle=col;ctx.strokeStyle=col;ctx.shadowColor=col;ctx.shadowBlur=7;
    const s=7;
    if(shape==='person'){
      ctx.beginPath();ctx.arc(0,-s*1.55,s*.65,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.roundRect(-s*.45,-s*.9,s*.9,s*1.35,2);ctx.fill();
      ctx.beginPath();
      ctx.moveTo(-s*.25,s*.45);ctx.lineTo(-s*.5,s*1.45);
      ctx.moveTo(s*.25,s*.45);ctx.lineTo(s*.5,s*1.45);
      ctx.lineWidth=s*.45;ctx.lineCap='round';ctx.stroke();
    }else if(shape==='circle'){
      ctx.beginPath();ctx.arc(0,0,s*.65,0,Math.PI*2);ctx.fill();
    }else if(shape==='triangle'){
      ctx.beginPath();ctx.moveTo(0,-s*.9);ctx.lineTo(s*.78,s*.45);ctx.lineTo(-s*.78,s*.45);ctx.closePath();ctx.fill();
    }else{
      ctx.beginPath();ctx.moveTo(0,-s*.9);ctx.lineTo(s*.55,0);ctx.lineTo(0,s*.9);ctx.lineTo(-s*.55,0);ctx.closePath();ctx.fill();
    }
    ctx.restore();
  }
}

function setup(){
  if(running)stop();
  tick=0;gd={sick:[],immune:[],healthy:[],total:[]};agents=[];
  const n=Math.round(gv('population'));
  const W=SIM.width,H=SIM.height;
  for(let i=0;i<n;i++)
    agents.push(new Agent(20+Math.random()*(W-40),20+Math.random()*(H-40),i===0?'sick':'healthy'));
  drawSim();drawGraph();updateStats();
}

function step(){
  const W=SIM.width,H=SIM.height;
  const inf=gv('infectiousness')/100,rec=gv('chanceRecover')/100,dur=gv('duration');
  agents.forEach(a=>a.move(W,H));
  agents.filter(a=>a.state==='sick').forEach(s=>{
    agents.forEach(o=>{
      if(o.state==='healthy'){
        const dx=s.x-o.x,dy=s.y-o.y;
        if(dx*dx+dy*dy<144&&Math.random()<inf){o.state='sick';o.infTick=tick;}
      }
    });
    if(tick-s.infTick>=dur&&Math.random()<rec)s.state='immune';
  });
  tick++;
  if(tick%2===0){
    const t=agents.length,
          ns=agents.filter(a=>a.state==='sick').length,
          ni=agents.filter(a=>a.state==='immune').length;
    gd.sick.push(ns);gd.immune.push(ni);gd.healthy.push(t-ns-ni);gd.total.push(t);
    if(gd.sick.length>300){gd.sick.shift();gd.immune.shift();gd.healthy.shift();gd.total.shift();}
  }
  updateStats();drawSim();drawGraph();
}

function updateStats(){
  const t=agents.length||1;
  const ns=agents.filter(a=>a.state==='sick').length,
        ni=agents.filter(a=>a.state==='immune').length;
  const pi=(ns/t*100).toFixed(1),pm=(ni/t*100).toFixed(1);
  document.getElementById('sInf').textContent=pi+'%';
  document.getElementById('sImm').textContent=pm+'%';
  document.getElementById('sTime').textContent=(tick/52).toFixed(2)+' yrs';
  document.getElementById('bInf').style.width=pi+'%';
  document.getElementById('bImm').style.width=pm+'%';
}

function drawSim(){
  sc.fillStyle=COL.bg;sc.fillRect(0,0,SIM.width,SIM.height);
  agents.forEach(a=>a.draw(sc));
}

function drawGraph(){
  const W=GRP.width,H=GRP.height;
  gc.fillStyle=COL.panel2;gc.fillRect(0,0,W,H);
  if(gd.sick.length<2)return;
  const pad={t:10,b:20,l:28,r:8},gW=W-pad.l-pad.r,gH=H-pad.t-pad.b,mx=agents.length||1;
  gc.strokeStyle='rgba(30,45,74,.7)';gc.lineWidth=.5;
  for(let i=0;i<=4;i++){
    const y=pad.t+(i/4)*gH;
    gc.beginPath();gc.moveTo(pad.l,y);gc.lineTo(W-pad.r,y);gc.stroke();
    gc.fillStyle='rgba(74,85,104,.9)';gc.font='8px Share Tech Mono';
    gc.fillText(Math.round(mx*(1-i/4)),2,y+3);
  }
  function line(arr,col){
    if(arr.length<2)return;
    gc.beginPath();gc.strokeStyle=col;gc.lineWidth=1.5;gc.shadowColor=col;gc.shadowBlur=4;
    arr.forEach((v,i)=>{
      const x=pad.l+(i/(arr.length-1))*gW,y=pad.t+gH-(v/mx)*gH;
      i===0?gc.moveTo(x,y):gc.lineTo(x,y);
    });
    gc.stroke();gc.shadowBlur=0;
  }
  line(gd.total,COL.total);line(gd.healthy,COL.healthy);
  line(gd.immune,COL.immune);line(gd.sick,COL.sick);
}

function loop(ts){
  if(!running)return;
  accum+=ts-(lastTs||ts);lastTs=ts;
  const iv=1000/(gv('speed')*8);
  while(accum>=iv){step();accum-=iv;}
  animId=requestAnimationFrame(loop);
}
function start(){
  if(running)return;running=true;lastTs=0;accum=0;
  document.getElementById('goBtn').textContent='⏸  PAUSE';
  document.getElementById('goBtn').classList.add('running');
  animId=requestAnimationFrame(loop);
}
function stop(){
  running=false;if(animId)cancelAnimationFrame(animId);
  document.getElementById('goBtn').textContent='▶  GO';
  document.getElementById('goBtn').classList.remove('running');
}

document.getElementById('goBtn').addEventListener('click',()=>{
  if(agents.length===0)setup();
  running?stop():start();
});
document.getElementById('setupBtn').addEventListener('click',setup);

function bindSlider(id,vid,sfx){
  const el=document.getElementById(id),vl=document.getElementById(vid);
  function u(){
    vl.textContent=el.value+(sfx||'');
    const p=(el.value-el.min)/(el.max-el.min)*100;
    el.style.setProperty('--p',p+'%');
  }
  el.addEventListener('input',u);u();
}
bindSlider('speed','vSpd','');
bindSlider('population','vPop','');
bindSlider('infectiousness','vInf','%');
bindSlider('chanceRecover','vRec','%');
bindSlider('duration','vDur','');

document.querySelectorAll('.sbtn').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('.sbtn').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');shape=b.dataset.shape;
  });
});

setup();
</script>
</body>
</html>"""

components.html(HTML, height=860, scrolling=False)
