import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="알록달록! 쓰레기 분류 게임",
    page_icon="🩷",
    layout="wide",
)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}
:root{--pink:#ff79b9;--hot:#f34d9c;--ink:#54295f;--cream:#fff8f3;--blue:#66c9ff;--yellow:#ffdb58}
body{margin:0;font-family:"Trebuchet MS","Malgun Gothic",sans-serif;background:#ffd7eb;color:var(--ink);user-select:none}
button{font:inherit;cursor:pointer}
.game-wrap{max-width:1180px;margin:0 auto;padding:14px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.logo{font-size:clamp(25px,4vw,44px);font-weight:1000;letter-spacing:-1.5px;color:#ff3d9b;text-shadow:2px 3px 0 white,4px 5px 0 #a7358a,-1px -1px 0 white}
.logo span{display:inline-block;background:#fff;border:3px solid #ef5eae;border-radius:22px;padding:7px 15px;box-shadow:0 5px 0 #c94891;transform:rotate(-1deg)}
.mission{background:linear-gradient(#fff5a9,#ffce48);border:3px solid #a45b31;border-radius:20px;padding:10px 17px;font-weight:1000;font-size:clamp(14px,2vw,21px);box-shadow:0 4px 0 #b86d3b}
.instructions{display:flex;align-items:center;gap:12px;background:#fff;border:3px solid #f17eb7;border-radius:22px;padding:10px 16px;margin-bottom:12px;box-shadow:0 5px 0 #d8589d}
.mascot{font-size:clamp(38px,6vw,64px)}
.instructions p{margin:0;font-size:clamp(14px,2vw,19px);font-weight:900;line-height:1.45}
.panel{border:5px solid #f17eb7;border-radius:28px;background:#fff9f5;padding:10px;box-shadow:0 8px 0 #c94891,inset 0 0 0 3px white;overflow:hidden}
.stage{height:600px;min-height:500px;position:relative;overflow:hidden;border:4px solid #e85fa9;border-radius:20px;background:linear-gradient(to bottom,#8de0ff 0%,#c8f3ff 27%,#ffb8d8 27%,#ffc9df 62%,#ffe6c5 62%,#ffdda8 100%);isolation:isolate}
.skyline{position:absolute;left:0;right:0;top:18%;height:17%;opacity:.55;background:linear-gradient(90deg,transparent 0 4%,#8cc8f4 4% 8%,transparent 8% 12%,#8cc8f4 12% 18%,transparent 18% 22%,#8cc8f4 22% 27%,transparent 27% 32%,#8cc8f4 32% 38%,transparent 38% 43%,#8cc8f4 43% 50%,transparent 50% 55%,#8cc8f4 55% 62%,transparent 62% 67%,#8cc8f4 67% 74%,transparent 74% 79%,#8cc8f4 79% 85%,transparent 85% 90%,#8cc8f4 90% 95%,transparent 95%)}
.window{position:absolute;top:4%;left:27%;width:43%;height:30%;background:linear-gradient(#7bd5ff,#d5f7ff);border:8px solid #fff4fa;border-radius:8px;box-shadow:0 0 0 4px #f47bb6;z-index:1}
.window:before,.window:after{content:"";position:absolute;background:#fff7fc;box-shadow:0 0 0 2px #f47bb6}
.window:before{width:7px;top:0;bottom:0;left:50%}.window:after{height:7px;left:0;right:0;top:53%}
.cloud{position:absolute;font-size:42px;opacity:.9}.c1{top:3%;left:32%}.c2{top:8%;right:30%}
.curtain{position:absolute;top:3%;height:32%;width:7%;z-index:2;background:repeating-linear-gradient(90deg,#ff86bd 0 10px,#ffd4e8 10px 20px);border:3px solid white;border-radius:0 0 18px 18px;box-shadow:0 3px 0 #dc579b}
.curtain.left{left:25%}.curtain.right{left:65%}
.walltiles{position:absolute;top:34%;left:0;right:0;height:27%;background-color:#ffb9d9;background-image:linear-gradient(#ff8ec2 2px,transparent 2px),linear-gradient(90deg,#ff8ec2 2px,transparent 2px);background-size:70px 45px;z-index:0}
.floor{position:absolute;left:0;right:0;bottom:0;height:39%;background-color:#ffe5c6;background-image:linear-gradient(90deg,transparent 49%,#f6b6b7 50%,transparent 51%),linear-gradient(#f7b6b6 2px,transparent 2px);background-size:120px 58px;border-top:10px solid #ffbf80}
.counter{position:absolute;left:0;right:0;top:58%;height:13%;background:linear-gradient(#ffdfa9,#ffbf79);border-top:7px solid #fff2d7;border-bottom:7px solid #ed9b67;z-index:1}
.sink{position:absolute;left:3%;top:38%;width:23%;height:25%;z-index:3;cursor:pointer;filter:drop-shadow(0 5px 0 #4383c5)}
.sink-top{position:absolute;inset:0;background:linear-gradient(#c8f1ff,#69bfff);border:5px solid #367ac5;border-radius:10px;box-shadow:inset 0 0 0 4px #fff}
.basin{position:absolute;left:13%;right:13%;top:14%;height:38%;background:linear-gradient(#498de0,#9fe4ff);border:5px solid #3475bf;border-radius:8px 8px 24px 24px}
.tap{position:absolute;left:45%;top:-18%;width:18%;height:28%;border:7px solid #3979c1;border-bottom:0;border-radius:18px 18px 0 0}
.tap:after{content:"";position:absolute;width:30px;height:10px;right:-25px;top:0;background:#5cb9ff;border:4px solid #3979c1;border-radius:8px}
.sink-label{position:absolute;left:14%;bottom:-18%;background:#4e9bff;color:white;border:4px solid #2455b6;border-radius:20px;padding:5px 17px;font-size:clamp(14px,2vw,22px);font-weight:1000;white-space:nowrap}
.plant{position:absolute;right:6%;top:30%;font-size:clamp(30px,4vw,55px);z-index:2}
.fridge{position:absolute;right:4%;top:32%;height:30%;width:13%;border:5px solid #ed72b2;border-radius:14px;background:linear-gradient(90deg,#ffadd5,#ffd9eb);z-index:2;box-shadow:inset 5px 0 white}
.fridge:before{content:"";position:absolute;top:48%;left:0;right:0;border-top:4px solid #ed72b2}
.fridge:after{content:"";position:absolute;top:18%;right:10%;height:22%;border-right:4px solid #d95a9b}
.heart{position:absolute;color:#ff4f9c;font-size:35px;text-shadow:2px 2px white;z-index:4}.h1{left:28%;top:39%}.h2{right:20%;top:37%}
.bin-row{position:absolute;left:7%;right:7%;bottom:4%;height:30%;display:flex;align-items:flex-end;justify-content:space-around;gap:3%;z-index:4}
.bin{position:relative;width:25%;height:88%;border:5px solid #4f234a;border-radius:18px 18px 28px 28px;box-shadow:0 7px 0 #8b4b71,inset 0 0 0 4px rgba(255,255,255,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;font-size:clamp(16px,2.5vw,27px);font-weight:1000;text-shadow:2px 2px #7e305f;transition:transform .15s,filter .15s}
.bin:before{content:"";position:absolute;top:-10%;left:-5%;width:110%;height:18%;border:5px solid #4f234a;border-radius:14px;background:inherit;filter:brightness(1.08)}
.bin .bin-icon{font-size:clamp(30px,5vw,55px);line-height:1.1}
.bin.vinyl{background:linear-gradient(90deg,#ff3d66,#ff6b8a)}.bin.plastic{background:linear-gradient(90deg,#ffc32e,#ffe15b);text-shadow:2px 2px #b77800}.bin.can{background:linear-gradient(90deg,#20c77b,#49e6a0)}
.bin.hover{transform:translateY(-10px) scale(1.04);filter:brightness(1.15)}
.trash{position:absolute;left:48%;top:42%;width:92px;height:120px;z-index:10;display:flex;align-items:center;justify-content:center;cursor:grab;touch-action:none;filter:drop-shadow(0 7px 4px #ad4c8a88);transform:rotate(-5deg)}
.trash:active{cursor:grabbing}.trash svg{width:100%;height:100%;overflow:visible}
.trash.dragging{z-index:20;filter:drop-shadow(0 10px 5px #aa4a8a99) brightness(1.04);transform:rotate(3deg) scale(1.06)}
.tipbar{display:flex;align-items:center;gap:12px;background:#fff;border:4px solid #f17eb7;border-radius:20px;padding:12px 16px;margin-top:12px;font-size:clamp(13px,1.8vw,19px);font-weight:900}
.tip-pill{background:#ff55a8;color:white;border:3px solid #a52e77;border-radius:18px;padding:4px 14px;box-shadow:0 3px 0 #b13c7f}
.overlay{position:absolute;inset:0;background:#ffeff8ef;z-index:30;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px}
.start-card{background:linear-gradient(#fff,#fff1f8);border:5px solid #f46caf;border-radius:30px;padding:25px;max-width:550px;width:90%;box-shadow:0 9px 0 #c94891}
.start-card h1{font-size:clamp(28px,5vw,52px);color:#ff3d9b;text-shadow:2px 3px white,4px 5px #b84b8b;margin:0 0 10px}
.start-card p{font-weight:900;font-size:clamp(15px,2vw,20px);line-height:1.6}
.preview{font-size:clamp(42px,7vw,68px);margin:8px 0 16px}
.big-button{border:4px solid #2455b6;border-radius:25px;background:linear-gradient(#7de0ff,#3c8bff);color:white;font-weight:1000;font-size:clamp(21px,3vw,30px);padding:12px 28px;text-shadow:2px 3px #2455b6;box-shadow:0 7px 0 #2449a3}
.big-button:active{transform:translateY(4px);box-shadow:0 3px 0 #2449a3}
.result{font-size:clamp(25px,4vw,42px);font-weight:1000;color:#ff3999;text-shadow:2px 2px white}
.small{font-size:13px;color:#7f4b77}
@media(max-width:650px){.game-wrap{padding:6px}.panel{padding:5px;border-width:3px}.stage{height:560px}.window{left:30%;width:42%}.sink{width:26%;height:22%;top:40%}.bin-row{left:2%;right:2%;gap:2%;height:25%}.bin{width:31%;font-size:14px;border-width:3px}.bin .bin-icon{font-size:32px}.trash{width:68px;height:95px;left:48%;top:44%}.sink-label{left:0;bottom:-23%;padding:4px 9px}.instructions{padding:8px}.fridge{width:15%;right:2%}.curtain.left{left:26%}.curtain.right{left:67%}}
</style>
</head>
<body>
<div class="game-wrap">
  <div class="topbar">
    <div class="logo"><span>♻ 알록달록 쓰레기 분류 게임!</span></div>
    <div class="mission">⭐ 미션: 쓰레기를 깨끗하게 분리배출</div>
  </div>
  <div class="instructions"><div class="mascot">🐰</div><p id="instruction">쓰레기를 잡고 드래그해서 <b>싱크대에 먼저 놓은 후</b>, 알맞은 쓰레기통에 쏙 넣어 주세요! 💗</p></div>
  <div class="panel">
    <div class="stage" id="stage">
      <div class="skyline"></div><div class="window"></div><div class="cloud c1">☁️</div><div class="cloud c2">☁️</div>
      <div class="curtain left"></div><div class="curtain right"></div><div class="walltiles"></div><div class="floor"></div>
      <div class="counter"></div><div class="plant">🪴</div><div class="fridge"></div><div class="heart h1">♥</div><div class="heart h2">♥</div>
      <div class="sink" id="sink" data-zone="sink"><div class="sink-top"></div><div class="basin"></div><div class="tap"></div><div class="sink-label">싱크대 🫧</div></div>
      <div class="bin-row">
        <div class="bin vinyl" data-zone="vinyl"><div class="bin-icon">🛍️</div><div>비닐</div></div>
        <div class="bin plastic" data-zone="plastic"><div class="bin-icon">🧴</div><div>플라스틱</div></div>
        <div class="bin can" data-zone="can"><div class="bin-icon">🥫</div><div>캔·고철</div></div>
      </div>
      <div class="trash" id="trash" aria-label="드래그할 쓰레기"></div>
      <div class="overlay" id="overlay">
        <div class="start-card">
          <h1>알록달록!<br>쓰레기 구조대</h1>
          <div class="preview">🐰 🫧 ♻️</div>
          <p>쓰레기를 싱크대에서 깨끗하게 씻은 뒤,<br>알맞은 분리수거함으로 옮겨 주세요!</p>
          <button class="big-button" id="startBtn">게임 시작! 🎮</button>
        </div>
      </div>
    </div>
  </div>
  <div class="tipbar"><span class="tip-pill">TIP</span><span id="tip">쓰레기를 드래그해 싱크대에 먼저 놓아 보세요!</span><span style="margin-left:auto">⭐ 점수: <b id="score">0</b></span></div>
</div>
<script>
(function(){
  const stage=document.getElementById('stage');
  const trash=document.getElementById('trash');
  const overlay=document.getElementById('overlay');
  const instruction=document.getElementById('instruction');
  const tip=document.getElementById('tip');
  const scoreEl=document.getElementById('score');
  const items=[
    {name:'과자 봉지',emoji:'🛍️',zone:'vinyl',color:'#ff6b8a',washed:false},
    {name:'플라스틱 병',emoji:'🧴',zone:'plastic',color:'#67c9ff',washed:false},
    {name:'음료 캔',emoji:'🥫',zone:'can',color:'#b7b7c9',washed:false},
    {name:'비닐 포장지',emoji:'🛍️',zone:'vinyl',color:'#ff6b8a',washed:false},
    {name:'샴푸 통',emoji:'🧴',zone:'plastic',color:'#67c9ff',washed:false},
    {name:'참치 캔',emoji:'🥫',zone:'can',color:'#b7b7c9',washed:false}
  ];
  let index=0,score=0,clean=false,dragging=false,pointerId=null,offsetX=0,offsetY=0;
  function drawItem(){
    if(index>=items.length){finish();return;}
    const item=items[index];
    trash.innerHTML='<div style="font-size:72px;line-height:1">'+item.emoji+'</div>';
    trash.style.left='48%';trash.style.top='42%';trash.style.width='92px';trash.style.height='120px';
    clean=false;
    instruction.innerHTML='쓰레기 <b>'+item.name+'</b>을(를) 잡고 싱크대에 먼저 놓아 주세요! 💗';
    tip.textContent='먼저 싱크대에서 쓰레기를 씻어 주세요!';
  }
  function finish(){
    trash.style.display='none';
    overlay.style.display='flex';
    overlay.innerHTML='<div class="start-card"><h1>미션 성공! 🎉</h1><div class="preview">🐰 🌈 ♻️</div><div class="result">'+score+' / '+items.length+'점</div><p>쓰레기 분리배출 미션을 완료했어요!<br>깨끗한 지구를 함께 지켜요. 🌍</p><button class="big-button" id="againBtn">다시 하기 🔄</button></div>';
    document.getElementById('againBtn').addEventListener('click',()=>{index=0;score=0;scoreEl.textContent='0';overlay.style.display='none';trash.style.display='flex';drawItem();});
  }
  function center(el){const r=el.getBoundingClientRect(),s=stage.getBoundingClientRect();return {x:r.left+r.width/2-s.left,y:r.top+r.height/2-s.top};}
  function overlaps(a,b){const x=center(a),y=center(b);const ar=a.getBoundingClientRect(),br=b.getBoundingClientRect();return Math.abs(x.x-y.x)<(ar.width+br.width)*.36&&Math.abs(x.y-y.y)<(ar.height+br.height)*.36;}
  function drop(){
    dragging=false;trash.classList.remove('dragging');
    document.querySelectorAll('.bin').forEach(b=>b.classList.remove('hover'));
    if(!clean){
      if(overlaps(trash,document.getElementById('sink'))){
        clean=true;scoreEl.textContent=score;
        instruction.innerHTML='잘했어요! 이제 <b>'+items[index].name+'</b>을(를) 알맞은 쓰레기통에 넣어 주세요! ✨';
        tip.textContent='이제 '+({vinyl:'비닐',plastic:'플라스틱',can:'캔·고철'}[items[index].zone])+' 통으로 옮겨 주세요!';
        trash.style.left='48%';trash.style.top='42%';
      }else{
        tip.textContent='앗! 먼저 싱크대에 놓아 깨끗하게 씻어 주세요.';
      }
      return;
    }
    const target=[...document.querySelectorAll('.bin')].find(b=>overlaps(trash,b));
    if(target){
      if(target.dataset.zone===items[index].zone){
        score++;scoreEl.textContent=score;
        tip.textContent='정답이에요! '+items[index].name+' 분리배출 성공! 🎉';
        index++;setTimeout(drawItem,650);
      }else{
        tip.textContent='다시 생각해 봐요! '+items[index].name+'은(는) 어느 통에 넣어야 할까요?';
        trash.style.left='48%';trash.style.top='42%';
      }
    }else{
      tip.textContent='쓰레기를 알맞은 쓰레기통 위에 놓아 주세요!';
    }
  }
  trash.addEventListener('pointerdown',e=>{
    if(overlay.style.display!=='none')return;
    dragging=true;pointerId=e.pointerId;trash.setPointerCapture(pointerId);trash.classList.add('dragging');
    const r=trash.getBoundingClientRect();offsetX=e.clientX-r.left;offsetY=e.clientY-r.top;e.preventDefault();
  });
  trash.addEventListener('pointermove',e=>{
    if(!dragging||e.pointerId!==pointerId)return;
    const s=stage.getBoundingClientRect();
    trash.style.left=(e.clientX-s.left-offsetX)+'px';
    trash.style.top=(e.clientY-s.top-offsetY)+'px';
    document.querySelectorAll('.bin').forEach(b=>b.classList.toggle('hover',overlaps(trash,b)));
  });
  trash.addEventListener('pointerup',e=>{if(dragging&&e.pointerId===pointerId)drop();});
  trash.addEventListener('pointercancel',()=>{if(dragging)drop();});
  document.getElementById('startBtn').addEventListener('click',()=>{overlay.style.display='none';drawItem();});
  drawItem();
})();
</script>
</body>
</html>
"""

components.html(html, height=850, scrolling=True)
