
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="알록달록! 쓰레기 구조대",
    page_icon="🧃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp {background:#72d8f5;}
.block-container {
    padding:0 !important;
    max-width:100% !important;
}
iframe {border:0 !important; width:100% !important;}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 게임 전체 화면
# ==========================================
html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* { box-sizing:border-box; }

:root {
    --ink:#493052;
    --blue:#1688ee;
    --blue-dark:#0757b2;
    --cream:#fff8d9;
    --outline:4px solid var(--ink);
}

body {
    margin:0;
    font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;
    color:var(--ink);
    background:#72d8f5;
    user-select:none;
    -webkit-user-select:none;
}

button {font-family:inherit; cursor:pointer;}

#game {
    width:100%;
    min-height:790px;
    overflow:hidden;
    position:relative;
    background:
      radial-gradient(circle at 12% 18%,#fff8c9 0 3px,transparent 4px),
      radial-gradient(circle at 88% 27%,#fff8c9 0 3px,transparent 4px),
      linear-gradient(#4fc8f4 0%,#a7edff 48%,#9be66f 48%,#55c96b 100%);
    background-size:43px 43px,57px 57px,100% 100%;
}

#game::before {
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background:repeating-linear-gradient(
      0deg,transparent 0 4px,rgba(36,81,117,.035) 4px 5px
    );
    z-index:80;
}

.screen {
    display:none;
    min-height:790px;
    padding:18px 18px 22px;
    position:relative;
    z-index:1;
}

.screen.active {display:flex; flex-direction:column; align-items:center;}

/* ===== 공통 레트로 게임 제목 ===== */
.logo {
    text-align:center;
    font-size:clamp(28px,5vw,49px);
    font-weight:1000;
    letter-spacing:-2px;
    line-height:1.25;
    color:#fff;
    -webkit-text-stroke:1px #573b69;
    text-shadow:
      3px 3px 0 #573b69,
      6px 6px 0 #2367ac,
      8px 9px 0 rgba(38,67,95,.2);
    margin:8px 0 5px;
}

.logo .rainbow {
    color:#ffec66;
    -webkit-text-stroke:1px #8a482a;
    text-shadow:
      3px 3px 0 #8a482a,
      6px 6px 0 #e56a38,
      8px 9px 0 rgba(38,67,95,.2);
}

.tagline {
    display:inline-block;
    background:#fff;
    border:3px solid var(--ink);
    border-radius:13px;
    padding:8px 17px;
    font-size:14px;
    font-weight:900;
    box-shadow:4px 4px 0 var(--ink);
    text-align:center;
    line-height:1.6;
}

/* ===== 첫 화면 ===== */
#start-screen {
    justify-content:flex-start;
    padding-top:22px;
}

.start-mascot {
    font-size:clamp(55px,10vw,90px);
    text-align:center;
    line-height:1.1;
    margin:8px 0 0;
    filter:drop-shadow(4px 5px 0 rgba(67,60,94,.2));
    animation:bob 1.8s ease-in-out infinite;
}

@keyframes bob {
    0%,100% {transform:translateY(0);}
    50% {transform:translateY(-7px);}
}

.start-card {
    width:min(100%,640px);
    margin:20px auto 0;
    padding:20px 16px;
    border:4px solid var(--ink);
    border-radius:20px;
    background:var(--cream);
    box-shadow:0 7px 0 var(--ink),0 13px 0 rgba(255,255,255,.5);
    text-align:center;
    position:relative;
}

.start-card::before {
    content:"★ TODAY'S MISSION ★";
    display:inline-block;
    background:#ffcf52;
    border:3px solid var(--ink);
    border-radius:8px;
    padding:6px 13px;
    font-size:12px;
    font-weight:1000;
    margin-top:-38px;
    margin-bottom:12px;
    box-shadow:3px 3px 0 var(--ink);
}

.start-description {
    font-size:15px;
    line-height:1.8;
    font-weight:900;
    margin:5px 0 15px;
}

.intro-bins {
    display:flex;
    justify-content:center;
    align-items:flex-end;
    gap:clamp(10px,4vw,35px);
    margin:18px 0 23px;
}

.bin {
    width:clamp(82px,22vw,133px);
    height:clamp(113px,24vw,150px);
    border:4px solid var(--ink);
    border-radius:12px 12px 20px 20px;
    position:relative;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    color:white;
    font-weight:1000;
    font-size:clamp(15px,2.7vw,21px);
    line-height:1.5;
    text-shadow:2px 2px 0 rgba(73,48,82,.35);
    box-shadow:0 7px 0 var(--ink);
}

.bin::before {
    content:"";
    position:absolute;
    left:-7px;
    right:-7px;
    top:-12px;
    height:17px;
    border:4px solid var(--ink);
    border-radius:8px;
    background:inherit;
}

.bin::after {
    content:"";
    position:absolute;
    left:11px;
    top:18px;
    bottom:12px;
    width:5px;
    border-radius:5px;
    background:rgba(255,255,255,.27);
}

.red {background:#f24d61;}
.yellow {background:#ffca35;}
.green {background:#23bd79;}

.bin-emoji {font-size:30px; margin-bottom:4px;}

.start-button {
    width:min(100%,330px);
    border:4px solid var(--ink);
    border-radius:15px;
    padding:15px 18px;
    background:linear-gradient(#48b8ff 0%,#1685f2 55%,#0870d8 56%,#0870d8 100%);
    color:white;
    font-size:25px;
    font-weight:1000;
    text-shadow:2px 2px 0 #0757a8;
    box-shadow:0 7px 0 var(--ink),inset 0 3px 0 rgba(255,255,255,.6);
    transition:transform .1s,filter .1s;
}

.start-button:hover {filter:brightness(1.1);}
.start-button:active {
    transform:translateY(5px);
    box-shadow:0 2px 0 var(--ink);
}

.start-tip {
    margin-top:19px;
    font-size:13px;
    font-weight:900;
    color:#73523b;
}

/* ===== 게임 화면 ===== */
#game-screen {padding-top:12px;}

.game-top {
    width:min(100%,1000px);
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:8px;
    margin-bottom:10px;
}

.pixel-button {
    border:3px solid var(--ink);
    border-radius:10px;
    background:#fff7c9;
    padding:9px 13px;
    font-weight:1000;
    font-size:13px;
    color:var(--ink);
    box-shadow:0 4px 0 var(--ink);
}

.pixel-button:active {transform:translateY(3px);box-shadow:0 1px 0 var(--ink);}

.mission-chip {
    border:3px solid var(--ink);
    border-radius:10px;
    background:#ffcf54;
    padding:8px 11px;
    font-weight:1000;
    font-size:13px;
    box-shadow:0 4px 0 var(--ink);
}

.game-heading {
    text-align:center;
    color:#fff;
    font-size:clamp(24px,4vw,34px);
    font-weight:1000;
    -webkit-text-stroke:1px var(--ink);
    text-shadow:3px 3px 0 var(--ink),5px 5px 0 #2585bd;
    margin:6px 0 12px;
}

.instruction {
    width:min(100%,670px);
    background:#fff9d9;
    border:3px solid var(--ink);
    border-radius:12px;
    padding:10px 12px;
    text-align:center;
    font-size:14px;
    font-weight:900;
    line-height:1.6;
    box-shadow:0 4px 0 var(--ink);
    margin-bottom:14px;
}

#stage {
    width:min(100%,1000px);
    height:480px;
    position:relative;
    overflow:hidden;
    border:5px solid var(--ink);
    border-radius:15px;
    background:#fff0cc;
    box-shadow:0 7px 0 var(--ink),0 12px 0 rgba(255,255,255,.55);
    isolation:isolate;
}

/* 주방의 벽과 바닥 */
#stage::before {
    content:"";
    position:absolute;
    inset:0 0 29% 0;
    background:
      radial-gradient(circle,#fff 0 2px,transparent 3px) 0 0/25px 25px,
      linear-gradient(#9fe6fa,#d8f7ff);
    z-index:-2;
}

#stage::after {
    content:"";
    position:absolute;
    left:0;right:0;bottom:0;
    height:31%;
    background:
      repeating-conic-gradient(#fff3d9 0 25%,#f5d9ad 0 50%) 0 0/46px 46px;
    border-top:5px solid #b57b4e;
    z-index:-1;
}

/* 창문 */
.window {
    position:absolute;
    top:18px;
    right:24%;
    width:105px;
    height:77px;
    border:6px solid #8e6048;
    background:linear-gradient(135deg,#7edbfa,#e4fbff);
    box-shadow:inset 0 0 0 3px #fff;
    pointer-events:none;
}

.window::before {
    content:"";
    position:absolute;
    left:50%;top:0;bottom:0;
    width:5px;background:#8e6048;
}

.window::after {
    content:"";
    position:absolute;
    top:50%;left:0;right:0;
    height:5px;background:#8e6048;
}

/* 싱크대: 왼쪽 */
#sink {
    position:absolute;
    left:16%;
    top:37%;
    transform:translate(-50%,-50%);
    width:clamp(125px,19%,175px);
    height:130px;
    border:5px solid #4b5483;
    border-radius:12px;
    background:linear-gradient(#d8f7ff 0 25%,#73bce8 26% 100%);
    box-shadow:0 7px 0 #4b5483,inset 0 4px 0 white;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    z-index:3;
    color:#253f73;
    font-weight:1000;
    transition:filter .1s,transform .1s;
}

#sink::before {
    content:"";
    position:absolute;
    top:-13px;
    left:-6px;right:-6px;
    height:15px;
    border:4px solid #4b5483;
    border-radius:7px;
    background:#9ed8f3;
}

.sink-icon {font-size:36px;line-height:1.2;}
.sink-label {
    margin-top:5px;
    border:2px solid #4b5483;
    background:#fff7d1;
    border-radius:7px;
    padding:3px 9px;
    font-size:16px;
}

#sink.drag-over {
    filter:brightness(1.13);
    transform:translate(-50%,-50%) scale(1.05);
    outline:5px solid #fff;
}

/* 쓰레기통은 무대 아래에 */
.stage-bin {
    position:absolute;
    bottom:18px;
    width:25%;
    max-width:170px;
    height:100px;
    border:5px solid var(--ink);
    border-radius:12px 12px 19px 19px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    color:white;
    font-weight:1000;
    font-size:clamp(13px,2vw,18px);
    line-height:1.35;
    text-shadow:2px 2px 0 rgba(73,48,82,.35);
    box-shadow:0 6px 0 var(--ink),inset 0 4px 0 rgba(255,255,255,.5);
    z-index:5;
    transition:transform .12s,filter .12s;
}

.stage-bin::before {
    content:"";
    position:absolute;
    left:-6px;right:-6px;top:-11px;
    height:14px;
    background:inherit;
    border:4px solid var(--ink);
    border-radius:8px;
}

#bin-red {left:2%;}
#bin-yellow {left:37.5%;}
#bin-green {right:2%;}

.stage-bin .bin-emoji {font-size:25px;margin-bottom:2px;}

.stage-bin.drag-over {
    transform:translateY(-7px) scale(1.04);
    filter:brightness(1.12);
    outline:4px solid white;
}

/* 쓰레기 오브젝트 */
#trash {
    position:absolute;
    left:61%;
    top:37%;
    width:90px;
    height:120px;
    z-index:20;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:grab;
    touch-action:none;
    -webkit-user-select:none;
    user-select:none;
}

#trash.dragging {
    cursor:grabbing;
    filter:drop-shadow(4px 6px 0 rgba(73,48,82,.3));
    z-index:30;
}

.trash-svg {
    width:100%;
    height:100%;
    overflow:visible;
    pointer-events:none;
}

/* 과자 봉지의 반짝임 */
#trash.bag-glow {
    animation:glitter .65s infinite alternate;
}

@keyframes glitter {
    from {
        filter:drop-shadow(0 0 5px #70efff)
               drop-shadow(0 0 10px #70efff);
    }
    to {
        filter:drop-shadow(0 0 13px #fff)
               drop-shadow(0 0 20px #50dcff)
               drop-shadow(0 0 28px #50dcff);
    }
}

/* 게임 하단 안내판 */
.tip-bar {
    width:min(100%,1000px);
    margin-top:15px;
    padding:10px 12px;
    border:3px solid var(--ink);
    border-radius:11px;
    background:#fff8d5;
    box-shadow:0 4px 0 var(--ink);
    text-align:center;
    font-size:13px;
    font-weight:900;
    line-height:1.5;
}

/* 성공/실패 오버레이 */
#result-overlay {
    display:none;
    position:absolute;
    inset:0;
    z-index:100;
    background:rgba(39,54,92,.68);
    align-items:center;
    justify-content:center;
    flex-direction:column;
    text-align:center;
}

#result-overlay.show {display:flex;}

.result-card {
    width:min(85%,420px);
    padding:28px 16px;
    background:#fff9dc;
    border:5px solid var(--ink);
    border-radius:20px;
    box-shadow:0 9px 0 var(--ink);
    animation:pop .25s ease-out;
}

#result-text {
    font-size:clamp(48px,10vw,78px);
    font-weight:1000;
    -webkit-text-stroke:1px var(--ink);
    text-shadow:4px 4px 0 rgba(73,48,82,.15);
    margin-bottom:10px;
}

#result-sub {
    font-size:16px;
    font-weight:1000;
    line-height:1.7;
}

@keyframes pop {
    from {transform:scale(.65) rotate(-5deg);opacity:0;}
    to {transform:scale(1) rotate(0);opacity:1;}
}

@media(max-width:540px) {
    #game,.screen {min-height:760px;}
    .screen {padding:14px 9px;}
    #stage {height:455px;}
    #sink {
        left:20%;
        top:36%;
        width:120px;
        height:110px;
    }
    #trash {width:75px;height:105px;}
    .stage-bin {
        width:31%;
        height:91px;
        bottom:15px;
    }
    #bin-red {left:1%;}
    #bin-yellow {left:34.5%;}
    #bin-green {right:1%;}
    .window {width:65px;height:58px;right:21%;}
    .instruction {font-size:13px;}
    .mission-chip,.pixel-button {font-size:11px;padding:8px;}
    .start-card {padding:17px 8px;}
}
</style>
</head>

<body>
<div id="game">

    <!-- 시작 화면 -->
    <section id="start-screen" class="screen active">
        <div class="start-mascot">🌎</div>

        <h1 class="logo">
            <span class="rainbow">알록달록!</span><br>
            쓰레기 구조대
        </h1>

        <div class="tagline">
            오늘의 미션! 쓰레기를 구해 주세요!
        </div>

        <div class="start-card">
            <p class="start-description">
                쓰레기를 깨끗하게 정리하고<br>
                알맞은 쓰레기통에 쏙 넣어 보세요!
            </p>

            <div class="intro-bins">
                <div class="bin red">
                    <div class="bin-emoji">🗑️</div>
                    비닐
                </div>
                <div class="bin yellow">
                    <div class="bin-emoji">🗑️</div>
                    플라스틱
                </div>
                <div class="bin green">
                    <div class="bin-emoji">🗑️</div>
                    캔, 고철
                </div>
            </div>

            <button id="start-button" class="start-button">
                ▶ 시작하기!
            </button>

            <p class="start-tip">
                💡 싱크대에 먼저 놓고, 알맞은 통으로 옮기기!
            </p>
        </div>
    </section>

    <!-- 게임 화면 -->
    <section id="game-screen" class="screen">
        <div class="game-top">
            <button id="home-button" class="pixel-button">
                🏠 처음으로
            </button>
            <span class="mission-chip">⭐ 미션 1 / 1</span>
        </div>

        <h2 class="game-heading">어디에 버릴까요?</h2>

        <div id="instruction" class="instruction">
            🧽 쓰레기를 잡고 싱크대에 먼저 놓아 주세요!
        </div>

        <div id="stage">
            <div class="window"></div>

            <!-- 싱크대 -->
            <div id="sink" data-zone="sink">
                <div class="sink-icon">🚰</div>
                <div class="sink-label">싱크대</div>
            </div>

            <!-- 분리배출 통 -->
            <div id="bin-red" class="stage-bin red" data-zone="red">
                <div class="bin-emoji">🗑️</div>
                비닐
            </div>

            <div id="bin-yellow" class="stage-bin yellow" data-zone="yellow">
                <div class="bin-emoji">🗑️</div>
                플라스틱
            </div>

            <div id="bin-green" class="stage-bin green" data-zone="green">
                <div class="bin-emoji">🗑️</div>
                캔, 고철
            </div>

            <!-- 랜덤 쓰레기가 나타나는 곳 -->
            <div id="trash"></div>
        </div>

        <div class="tip-bar">
            💡 TIP : 먼저 싱크대에서 정리한 뒤 알맞은 쓰레기통으로 옮겨 주세요!
        </div>
    </section>

    <!-- 결과 팝업 -->
    <div id="result-overlay">
        <div class="result-card">
            <div id="result-text">성공! 🎉</div>
            <div id="result-sub">지구가 기뻐하고 있어요!</div>
        </div>
    </div>
</div>

<script>
// ==========================================
// 3. 쓰레기 그림: SVG로 직접 그려요.
// ==========================================

const pictures = {
    juice: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <rect x="39" y="5" width="22" height="13" rx="3" fill="#579447"/>
      <path d="M38 17 L62 17 L62 30 Q70 37 72 47 L75 104 Q75 115 64 116 L36 116 Q25 115 25 104 L28 47 Q30 37 38 30 Z"
        fill="#ffad42" stroke="#8e4c2c" stroke-width="3"/>
      <path d="M34 45 Q32 58 33 73" fill="none" stroke="#ffe6ac" stroke-width="5" stroke-linecap="round"/>
      <rect x="28" y="60" width="44" height="30" rx="5" fill="#fff2c9" stroke="#8e4c2c" stroke-width="2"/>
      <circle cx="50" cy="75" r="10" fill="#ff9c25"/>
      <path d="M50 65 L50 85 M40 75 L60 75 M43 68 L57 82 M57 68 L43 82"
        stroke="#ffe5a3" stroke-width="1.5"/>
      <text x="50" y="99" text-anchor="middle" font-size="7" fill="#a95d20" font-weight="bold">ORANGE</text>
    </svg>`,

    emptyBottle: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <rect x="40" y="5" width="20" height="12" rx="3" fill="#78b875" stroke="#493052" stroke-width="2"/>
      <path d="M39 17 L61 17 L61 30 Q69 38 71 47 L74 103 Q75 115 64 116 L36 116 Q25 115 26 103 L29 47 Q31 38 39 30 Z"
        fill="#d8f2ed" fill-opacity=".85" stroke="#493052" stroke-width="3"/>
      <path d="M35 43 Q32 62 35 95" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
      <path d="M33 35 L67 35 M31 43 L69 43" stroke="#a5d7cc" stroke-width="2"/>
      <path d="M36 103 L64 103" stroke="#a5d7cc" stroke-width="2"/>
    </svg>`,

    cola: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <path d="M25 18 Q23 22 24 28 L28 105 Q29 113 37 115 L63 115 Q71 113 72 105 L76 28 Q77 22 75 18 Z"
        fill="#d72e39" stroke="#493052" stroke-width="3"/>
      <ellipse cx="50" cy="19" rx="24" ry="6" fill="#eee" stroke="#493052" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="11" ry="3" fill="#a4a4a4"/>
      <path d="M30 34 Q35 44 34 60" fill="none" stroke="#f98c91" stroke-width="4" stroke-linecap="round"/>
      <text x="50" y="73" text-anchor="middle" font-size="15" font-weight="900" fill="white">COLA</text>
      <path d="M29 104 Q50 110 71 104" stroke="#f7a0a4" stroke-width="2" fill="none"/>
    </svg>`,

    plainCan: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <defs>
        <linearGradient id="metal" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#9babb2"/>
          <stop offset=".35" stop-color="#f5f8f8"/>
          <stop offset=".7" stop-color="#c6d0d4"/>
          <stop offset="1" stop-color="#899da4"/>
        </linearGradient>
      </defs>
      <path d="M27 18 Q25 23 26 29 L29 104 Q30 113 38 115 L62 115 Q70 113 71 104 L74 29 Q75 23 73 18 Z"
        fill="url(#metal)" stroke="#493052" stroke-width="3"/>
      <ellipse cx="50" cy="19" rx="23" ry="7" fill="#e8eded" stroke="#493052" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="10" ry="3" fill="#9eacb0"/>
      <path d="M32 33 L35 98" stroke="#fff" stroke-width="4"/>
      <path d="M30 105 Q50 111 70 105" stroke="#87989d" stroke-width="2" fill="none"/>
    </svg>`,

    bag: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <path d="M20 20 L80 20 L85 31 L81 101 L73 110 L27 110 L19 101 L15 31 Z"
        fill="#f4bd52" stroke="#493052" stroke-width="3"/>
      <path d="M20 20 L80 20 L76 29 L24 29 Z" fill="#ffe5a0"/>
      <path d="M19 100 L81 100 L73 110 L27 110 Z" fill="#e6a73d"/>
      <rect x="23" y="41" width="54" height="43" rx="8" fill="#fff4d5" stroke="#493052" stroke-width="2"/>
      <circle cx="50" cy="61" r="13" fill="#ee7c45"/>
      <circle cx="45" cy="57" r="2" fill="#fff1c4"/>
      <circle cx="55" cy="57" r="2" fill="#fff1c4"/>
      <path d="M45 66 Q50 71 55 66" stroke="#fff1c4" stroke-width="2" fill="none" stroke-linecap="round"/>
      <text x="50" y="95" text-anchor="middle" font-size="8" font-weight="900" fill="#996124">SNACK</text>
    </svg>`
};

// ==========================================
// 4. 게임 상태
// ==========================================

const startScreen = document.getElementById("start-screen");
const gameScreen = document.getElementById("game-screen");
const startButton = document.getElementById("start-button");
const homeButton = document.getElementById("home-button");
const stage = document.getElementById("stage");
const trash = document.getElementById("trash");
const instruction = document.getElementById("instruction");
const overlay = document.getElementById("result-overlay");
const resultText = document.getElementById("result-text");
const resultSub = document.getElementById("result-sub");

let currentTrash = null;
let cleaned = false;
let gameOver = false;
let dragging = false;
let offsetX = 0;
let offsetY = 0;
let resultTimer = null;

// 정답 쓰레기통
const trashTypes = [
    {id:"juice", answer:"yellow"},
    {id:"cola", answer:"green"},
    {id:"bag", answer:"red"}
];

// ==========================================
// 5. 화면 전환
// ==========================================

function showStartScreen() {
    clearTimeout(resultTimer);
    overlay.classList.remove("show");
    gameScreen.classList.remove("active");
    startScreen.classList.add("active");
    gameOver = false;
    dragging = false;
}

function startGame() {
    clearTimeout(resultTimer);
    overlay.classList.remove("show");

    startScreen.classList.remove("active");
    gameScreen.classList.add("active");

    // 세 종류 중 하나를 무작위로 골라요.
    currentTrash = trashTypes[
        Math.floor(Math.random() * trashTypes.length)
    ];

    cleaned = false;
    gameOver = false;
    dragging = false;

    trash.innerHTML = pictures[currentTrash.id];
    trash.classList.remove("bag-glow","dragging");
    trash.style.display = "flex";
    trash.style.visibility = "visible";
    trash.style.left = "61%";
    trash.style.top = "37%";
    trash.style.transform = "translate(-50%,-50%)";

    instruction.innerHTML =
        "🧽 쓰레기를 잡고 <b>왼쪽 싱크대</b>에 먼저 놓아 주세요!";
}

// ==========================================
// 6. 결과 표시
// ==========================================

function finishGame(success) {
    if (gameOver) return;

    gameOver = true;
    dragging = false;

    resultText.textContent = success ? "성공! 🎉" : "실패! 😭";
    resultText.style.color = success ? "#27ad72" : "#ef5267";
    resultSub.textContent = success
        ? "지구가 기뻐하고 있어요!"
        : "다시 도전해 봐요!";

    overlay.classList.add("show");

    // 결과를 3초 동안 보여준 뒤 첫 화면으로 돌아가요.
    resultTimer = setTimeout(showStartScreen, 3000);
}

// ==========================================
// 7. 드롭 위치 확인
//    쓰레기를 잠시 숨겨서 아래쪽 대상을 찾아요.
// ==========================================

function getDropZone(clientX, clientY) {
    const oldVisibility = trash.style.visibility;
    trash.style.visibility = "hidden";

    const element = document.elementFromPoint(clientX, clientY);

    trash.style.visibility = oldVisibility;

    if (!element) return null;

    const zone = element.closest("[data-zone]");

    if (!zone || !stage.contains(zone)) return null;

    return zone.dataset.zone;
}

// ==========================================
// 8. 싱크대와 쓰레기통 처리
// ==========================================

function handleDrop(zone) {
    if (gameOver || !currentTrash || !zone) return;

    // 첫 번째 단계: 싱크대를 먼저 거쳐야 해요.
    if (!cleaned) {
        if (zone === "sink") {
            cleaned = true;

            if (currentTrash.id === "juice") {
                trash.innerHTML = pictures.emptyBottle;
                instruction.innerHTML =
                    "✨ 주스를 비웠어요! 빈 페트병을 <b>노란색 플라스틱 통</b>에 넣어요!";
            } else if (currentTrash.id === "cola") {
                trash.innerHTML = pictures.plainCan;
                instruction.innerHTML =
                    "✨ 캔을 정리했어요! 일반 캔을 <b>초록색 캔·고철 통</b>에 넣어요!";
            } else {
                trash.classList.add("bag-glow");
                instruction.innerHTML =
                    "✨ 반짝반짝! 과자 봉지를 <b>빨간색 비닐 통</b>에 넣어요!";
            }

            // 정리한 쓰레기를 다시 잡기 편한 위치에 놓아요.
            trash.style.left = "54%";
            trash.style.top = "37%";
            trash.style.transform = "translate(-50%,-50%)";
        } else {
            // 싱크대를 거치지 않고 통에 넣으면 실패예요.
            finishGame(false);
        }

        return;
    }

    // 두 번째 단계: 정답 통인지 확인해요.
    if (zone === "red" || zone === "yellow" || zone === "green") {
        finishGame(zone === currentTrash.answer);
    } else if (zone === "sink") {
        // 싱크대에 다시 놓으면 처리된 상태를 유지해요.
        trash.style.left = "54%";
        trash.style.top = "37%";
        trash.style.transform = "translate(-50%,-50%)";
    }
}

// ==========================================
// 9. 마우스와 터치 드래그
// ==========================================

trash.addEventListener("pointerdown", function(event) {
    if (gameOver || !currentTrash) return;

    event.preventDefault();

    dragging = true;
    trash.classList.add("dragging");

    const rect = trash.getBoundingClientRect();
    offsetX = event.clientX - rect.left;
    offsetY = event.clientY - rect.top;

    // 손가락이나 마우스가 쓰레기 밖으로 나가도 계속 추적해요.
    try {
        trash.setPointerCapture(event.pointerId);
    } catch (error) {
        // 포인터 캡처를 사용할 수 없는 환경도 처리해요.
    }
});

trash.addEventListener("pointermove", function(event) {
    if (!dragging || gameOver) return;

    event.preventDefault();

    const rect = stage.getBoundingClientRect();

    let x = event.clientX - rect.left - offsetX;
    let y = event.clientY - rect.top - offsetY;

    x = Math.max(0, Math.min(rect.width - trash.offsetWidth, x));
    y = Math.max(0, Math.min(rect.height - trash.offsetHeight, y));

    trash.style.left = x + "px";
    trash.style.top = y + "px";
    trash.style.transform = "none";

    // 현재 놓을 수 있는 싱크대나 쓰레기통을 강조해요.
    document.querySelectorAll("[data-zone]").forEach(function(el) {
        el.classList.remove("drag-over");
    });

    const zone = getDropZone(event.clientX, event.clientY);

    if (zone) {
        const target = document.querySelector(
            '[data-zone="' + zone + '"]'
        );
        if (target) target.classList.add("drag-over");
    }
});

function endDrag(event) {
    if (!dragging) return;

    dragging = false;
    trash.classList.remove("dragging");

    document.querySelectorAll("[data-zone]").forEach(function(el) {
        el.classList.remove("drag-over");
    });

    // 손을 뗀 좌표를 사용해 정확히 판정해요.
    const zone = getDropZone(event.clientX, event.clientY);

    if (zone) {
        handleDrop(zone);
    } else {
        // 목표 영역 밖이면 원래 위치로 돌아가요.
        trash.style.left = "61%";
        trash.style.top = "37%";
        trash.style.transform = "translate(-50%,-50%)";
    }
}

trash.addEventListener("pointerup", endDrag);

trash.addEventListener("pointercancel", function() {
    dragging = false;
    trash.classList.remove("dragging");

    document.querySelectorAll("[data-zone]").forEach(function(el) {
        el.classList.remove("drag-over");
    });
});

// ==========================================
// 10. 버튼 이벤트
// ==========================================

startButton.addEventListener("click", startGame);
homeButton.addEventListener("click", showStartScreen);

// 처음에는 시작 화면을 보여 줘요.
showStartScreen();
</script>
</body>
</html>
"""

# ==========================================
# 3. Streamlit에 게임 표시
# ==========================================
components.html(
    html,
    height=810,
    scrolling=True,
)
