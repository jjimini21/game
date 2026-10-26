
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="알록달록 쓰레기 분류 게임",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 페이지 여백과 기본 Streamlit 요소 숨기기
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {
            background: #fff8e9;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. 게임 화면
#    HTML, CSS, JavaScript를 한 파일에 포함
# ==========================================

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: "Apple SD Gothic Neo", "Malgun Gothic",
                 "Nanum Gothic", sans-serif;
    color: #594536;
    background: #fff8e9;
}

button {
    font-family: inherit;
    cursor: pointer;
}

#app {
    width: 100%;
    min-height: 760px;
    overflow: hidden;
    background: linear-gradient(180deg, #fff8e9 0%, #ffefd4 100%);
    position: relative;
}

h1, h2, p {
    margin-top: 0;
}

.screen {
    display: none;
    min-height: 760px;
    padding: 24px 18px;
    position: relative;
}

.screen.active {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* 제목과 안내 문구 */
.game-title {
    text-align: center;
    color: #76513c;
    font-size: clamp(25px, 4vw, 38px);
    font-weight: 900;
    margin: 10px 0 8px;
}

.subtitle {
    text-align: center;
    color: #9b7960;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 18px;
}

/* 첫 화면의 쓰레기통 */
.intro-bins {
    display: flex;
    align-items: end;
    justify-content: center;
    gap: clamp(12px, 4vw, 35px);
    width: 100%;
    margin: 25px auto 28px;
}

.bin {
    width: clamp(90px, 22vw, 155px);
    height: clamp(125px, 27vw, 190px);
    border-radius: 16px 16px 24px 24px;
    border: 5px solid rgba(255,255,255,.65);
    box-shadow: 0 9px 0 rgba(98,70,45,.12),
                0 12px 18px rgba(98,70,45,.12);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    color: white;
    font-size: clamp(17px, 3vw, 24px);
    font-weight: 900;
    text-align: center;
    line-height: 1.5;
    text-shadow: 0 2px 3px rgba(0,0,0,.13);
}

.bin::before {
    content: "";
    position: absolute;
    top: -13px;
    left: -7px;
    right: -7px;
    height: 18px;
    border-radius: 9px;
    background: inherit;
    border: 3px solid rgba(255,255,255,.65);
}

.bin::after {
    content: "";
    position: absolute;
    top: 22px;
    bottom: 14px;
    left: 10px;
    width: 5px;
    border-radius: 8px;
    background: rgba(255,255,255,.22);
}

.red { background: #ef6262; }
.yellow { background: #efb92f; }
.green { background: #55ae79; }

.bin-emoji {
    font-size: clamp(26px, 5vw, 42px);
    margin-bottom: 5px;
}

/* 시작 버튼 */
.start-button {
    border: none;
    border-radius: 50px;
    padding: 17px 54px;
    background: #ff9d58;
    color: white;
    font-size: 23px;
    font-weight: 900;
    box-shadow: 0 6px 0 #df7b3e;
    transition: transform .15s;
}

.start-button:hover {
    transform: translateY(-3px);
}

.start-button:active {
    transform: translateY(3px);
    box-shadow: 0 2px 0 #df7b3e;
}

.tip {
    margin-top: 24px;
    color: #9b7960;
    font-size: 14px;
    text-align: center;
}

/* 게임 화면 상단 */
.top-row {
    width: min(100%, 850px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.back-button {
    border: 2px solid #edd9bd;
    color: #87664d;
    background: #fffdf8;
    border-radius: 25px;
    padding: 10px 15px;
    font-size: 14px;
    font-weight: bold;
}

.step-label {
    background: #fff;
    border: 2px solid #f4dfbd;
    border-radius: 30px;
    padding: 9px 16px;
    color: #9b704a;
    font-size: 14px;
    font-weight: bold;
}

.instruction {
    background: #fff;
    border: 2px solid #f3dfc1;
    border-radius: 18px;
    padding: 12px 18px;
    text-align: center;
    width: min(100%, 560px);
    font-size: 15px;
    line-height: 1.6;
    margin: 12px 0 10px;
}

/* 게임 무대 */
#stage {
    width: min(100%, 900px);
    height: 470px;
    flex-shrink: 0;
    position: relative;
    overflow: hidden;
    border: 4px solid #f0d9b9;
    border-radius: 24px;
    background:
        linear-gradient(180deg, #fff9ed 0%, #fff1d9 74%, #e8cda8 74%);
    box-shadow: inset 0 -6px 0 rgba(151,108,65,.08);
}

/* 벽 장식 */
.wall-window {
    position: absolute;
    top: 22px;
    right: 22px;
    width: 85px;
    height: 75px;
    border: 7px solid #e4c59e;
    border-radius: 9px;
    background: linear-gradient(135deg, #bce8e5, #e4f7e9);
}

.wall-window::before {
    content: "";
    position: absolute;
    left: 50%;
    height: 100%;
    width: 5px;
    background: #e4c59e;
}

.wall-window::after {
    content: "";
    position: absolute;
    top: 50%;
    height: 5px;
    width: 100%;
    background: #e4c59e;
}

.wall-shelf {
    position: absolute;
    top: 122px;
    right: 18px;
    width: 115px;
    height: 9px;
    border-radius: 5px;
    background: #d3ad80;
}

/* 싱크대 */
#sink {
    position: absolute;
    left: 50%;
    top: 43%;
    transform: translate(-50%, -50%);
    width: clamp(155px, 28%, 225px);
    height: 125px;
    border-radius: 13px 13px 20px 20px;
    background: #b9dce0;
    border: 7px solid #8fb9c0;
    box-shadow: 0 8px 0 rgba(91,143,151,.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #477a83;
    font-weight: 900;
    z-index: 1;
    transition: .15s;
}

#sink .sink-icon {
    font-size: 32px;
    line-height: 1.2;
}

#sink .sink-label {
    font-size: 18px;
    margin-top: 3px;
}

#sink.drag-over {
    background: #d5f6f5;
    border-color: #4cbfc9;
    box-shadow: 0 0 0 7px rgba(93,214,222,.25);
}

/* 게임 무대의 쓰레기통 */
.stage-bin {
    position: absolute;
    bottom: 18px;
    width: 23%;
    max-width: 155px;
    height: 105px;
    border-radius: 12px 12px 18px 18px;
    border: 4px solid rgba(255,255,255,.72);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    color: white;
    text-align: center;
    font-weight: 900;
    font-size: clamp(13px, 2vw, 17px);
    line-height: 1.4;
    box-shadow: 0 6px 0 rgba(90,65,43,.14);
    z-index: 2;
}

.stage-bin::before {
    content: "";
    position: absolute;
    top: -10px;
    left: -5px;
    right: -5px;
    height: 13px;
    background: inherit;
    border: 3px solid rgba(255,255,255,.7);
    border-radius: 7px;
}

#bin-red { left: 3%; }
#bin-yellow { left: 38.5%; }
#bin-green { right: 3%; }

.stage-bin.drag-over {
    outline: 5px solid #fff;
    transform: translateY(-5px);
}

.stage-bin .bin-emoji {
    font-size: 27px;
    margin-bottom: 0;
}

/* 드래그하는 쓰레기 */
#trash {
    position: absolute;
    left: 50%;
    top: 43%;
    transform: translate(-50%, -50%);
    width: 100px;
    height: 125px;
    z-index: 5;
    cursor: grab;
    touch-action: none;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: filter .15s;
}

#trash:active {
    cursor: grabbing;
}

#trash.dragging {
    filter: drop-shadow(0 9px 7px rgba(0,0,0,.18));
    z-index: 20;
}

.trash-svg {
    width: 100%;
    height: 100%;
    overflow: visible;
    pointer-events: none;
}

#trash.bag-glow {
    filter: drop-shadow(0 0 7px #75eaff)
            drop-shadow(0 0 16px #53dfff)
            drop-shadow(0 0 25px #a2f5ff);
    animation: sparkle 1s infinite alternate;
}

@keyframes sparkle {
    from { filter: drop-shadow(0 0 5px #75eaff)
                   drop-shadow(0 0 12px #53dfff); }
    to { filter: drop-shadow(0 0 13px #75eaff)
                 drop-shadow(0 0 25px #53dfff)
                 drop-shadow(0 0 35px #a2f5ff); }
}

/* 결과 메시지 */
#result-overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: rgba(255,248,233,.88);
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

#result-overlay.show {
    display: flex;
    animation: appear .2s ease-out;
}

#result-text {
    font-size: clamp(48px, 10vw, 82px);
    font-weight: 1000;
    margin-bottom: 12px;
    text-shadow: 0 5px 0 rgba(100,70,40,.08);
}

#result-sub {
    color: #85684f;
    font-size: 18px;
    font-weight: bold;
}

@keyframes appear {
    from { opacity: 0; transform: scale(.92); }
    to { opacity: 1; transform: scale(1); }
}

.bottom-note {
    text-align: center;
    font-size: 13px;
    color: #a18469;
    padding: 10px 0 0;
}

@media (max-width: 520px) {
    #app, .screen { min-height: 720px; }
    #stage { height: 420px; }
    #sink { top: 40%; height: 110px; }
    #trash { top: 40%; width: 82px; height: 108px; }
    .stage-bin { height: 90px; bottom: 14px; }
    .wall-window { width: 58px; height: 55px; }
    .wall-shelf { top: 100px; width: 75px; }
    .instruction { font-size: 13px; }
}
</style>
</head>

<body>
<div id="app">

    <!-- 첫 화면 -->
    <section id="start-screen" class="screen active">
        <div style="font-size:48px; margin-top:15px;">♻️</div>
        <h1 class="game-title">알록달록 쓰레기 분류 게임</h1>
        <p class="subtitle">
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

        <button id="start-button" class="start-button">시작하기 ✨</button>
        <p class="tip">💡 힌트: 쓰레기는 먼저 싱크대에서 처리해야 해요!</p>
    </section>

    <!-- 게임 화면 -->
    <section id="game-screen" class="screen">
        <div class="top-row">
            <button id="home-button" class="back-button">← 처음으로</button>
            <span class="step-label">미션: 쓰레기 분리배출</span>
        </div>

        <h1 class="game-title" style="margin-top:12px;">어디에 버려야 할까요?</h1>
        <p class="subtitle" style="margin-bottom:5px;">
            쓰레기를 드래그해서 싱크대에 놓은 뒤, 알맞은 통으로 옮겨요!
        </p>

        <div class="instruction" id="instruction">
            🧽 먼저 쓰레기를 싱크대에 드래그해 주세요.
        </div>

        <div id="stage">
            <div class="wall-window"></div>
            <div class="wall-shelf"></div>

            <!-- 쓰레기를 먼저 놓아야 하는 싱크대 -->
            <div id="sink" data-zone="sink">
                <div class="sink-icon">🚰</div>
                <div class="sink-label">싱크대</div>
            </div>

            <!-- 쓰레기통 3개 -->
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

            <!-- JavaScript에서 쓰레기 그림을 넣어요 -->
            <div id="trash" draggable="true" aria-label="드래그할 쓰레기"></div>
        </div>

        <p class="bottom-note">
            🧡 작은 실천이 지구를 웃게 만들어요!
        </p>
    </section>

    <!-- 성공 또는 실패 메시지 -->
    <div id="result-overlay">
        <div id="result-text">성공!</div>
        <div id="result-sub">참 잘했어요!</div>
    </div>
</div>

<script>
// ==========================================
// 3. 쓰레기 그림 만들기
//    외부 이미지 파일 없이 SVG로 표현해요.
// ==========================================

const pictures = {
    juice: `
    <svg class="trash-svg" viewBox="0 0 100 125" aria-label="오렌지 주스 페트병">
      <defs>
        <linearGradient id="juiceBottle" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#e4a13e"/>
          <stop offset=".45" stop-color="#ffbd58"/>
          <stop offset="1" stop-color="#e99531"/>
        </linearGradient>
      </defs>
      <rect x="39" y="5" width="22" height="13" rx="3" fill="#5f9a48"/>
      <path d="M38 17 L62 17 L62 30 Q70 37 72 47 L75 104 Q75 115 64 116 L36 116 Q25 115 25 104 L28 47 Q30 37 38 30 Z"
            fill="url(#juiceBottle)" stroke="#d88a29" stroke-width="2"/>
      <path d="M37 24 L63 24 L63 32 L37 32 Z" fill="#ffd48a" opacity=".8"/>
      <path d="M34 45 Q32 58 33 73" fill="none" stroke="#ffe6ac" stroke-width="5" stroke-linecap="round"/>
      <rect x="28" y="60" width="44" height="30" rx="5" fill="#fff2c9"/>
      <circle cx="50" cy="75" r="10" fill="#ff9c25"/>
      <path d="M50 65 L50 85 M40 75 L60 75 M43 68 L57 82 M57 68 L43 82"
            stroke="#ffe5a3" stroke-width="1.5"/>
      <text x="50" y="99" text-anchor="middle" font-size="7" fill="#a95d20" font-weight="bold">ORANGE</text>
    </svg>`,

    emptyBottle: `
    <svg class="trash-svg" viewBox="0 0 100 125" aria-label="빈 페트병">
      <rect x="40" y="5" width="20" height="12" rx="3" fill="#78b875"/>
      <path d="M39 17 L61 17 L61 30 Q69 38 71 47 L74 103 Q75 115 64 116 L36 116 Q25 115 26 103 L29 47 Q31 38 39 30 Z"
            fill="#d8f2ed" fill-opacity=".7" stroke="#77b9ad" stroke-width="2.5"/>
      <path d="M35 43 Q32 62 35 95" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
      <path d="M33 35 L67 35 M31 43 L69 43" stroke="#a5d7cc" stroke-width="2"/>
      <path d="M36 103 L64 103" stroke="#a5d7cc" stroke-width="2"/>
    </svg>`,

    cola: `
    <svg class="trash-svg" viewBox="0 0 100 125" aria-label="콜라 캔">
      <ellipse cx="50" cy="18" rx="25" ry="8" fill="#d8d8d8" stroke="#999" stroke-width="2"/>
      <path d="M25 18 Q23 22 24 28 L28 105 Q29 113 37 115 L63 115 Q71 113 72 105 L76 28 Q77 22 75 18 Z"
            fill="#d72e39" stroke="#a9212d" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="24" ry="6" fill="#eeeeee" stroke="#aaa" stroke-width="1.5"/>
      <ellipse cx="50" cy="19" rx="11" ry="3" fill="#a4a4a4"/>
      <path d="M30 34 Q35 44 34 60" fill="none" stroke="#f98c91" stroke-width="4" stroke-linecap="round"/>
      <text x="50" y="73" text-anchor="middle" font-size="15" font-weight="900" fill="white">COLA</text>
      <path d="M29 104 Q50 110 71 104" stroke="#f7a0a4" stroke-width="2" fill="none"/>
    </svg>`,

    plainCan: `
    <svg class="trash-svg" viewBox="0 0 100 125" aria-label="라벨을 제거한 일반 캔">
      <defs>
        <linearGradient id="canMetal" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#9babb2"/>
          <stop offset=".35" stop-color="#f5f8f8"/>
          <stop offset=".7" stop-color="#c6d0d4"/>
          <stop offset="1" stop-color="#899da4"/>
        </linearGradient>
      </defs>
      <path d="M27 18 Q25 23 26 29 L29 104 Q30 113 38 115 L62 115 Q70 113 71 104 L74 29 Q75 23 73 18 Z"
            fill="url(#canMetal)" stroke="#84979e" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="23" ry="7" fill="#e8eded" stroke="#84979e" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="10" ry="3" fill="#9eacb0"/>
      <path d="M32 33 L35 98" stroke="#fff" stroke-width="4" opacity=".85"/>
      <path d="M30 105 Q50 111 70 105" stroke="#87989d" stroke-width="2" fill="none"/>
    </svg>`,

    bag: `
    <svg class="trash-svg" viewBox="0 0 100 125" aria-label="과자 봉지">
      <path d="M20 20 L80 20 L85 31 L81 101 L73 110 L27 110 L19 101 L15 31 Z"
            fill="#f4bd52" stroke="#d99b31" stroke-width="2.5"/>
      <path d="M20 20 L80 20 L76 29 L24 29 Z" fill="#ffe5a0"/>
      <path d="M19 100 L81 100 L73 110 L27 110 Z" fill="#e6a73d"/>
      <path d="M20 35 L80 35" stroke="#fff1c4" stroke-width="2"/>
      <rect x="23" y="41" width="54" height="43" rx="8" fill="#fff4d5"/>
      <circle cx="50" cy="61" r="13" fill="#ee7c45"/>
      <circle cx="45" cy="57" r="2" fill="#fff1c4"/>
      <circle cx="55" cy="57" r="2" fill="#fff1c4"/>
      <path d="M45 66 Q50 71 55 66" stroke="#fff1c4" stroke-width="2" fill="none" stroke-linecap="round"/>
      <text x="50" y="95" text-anchor="middle" font-size="8" font-weight="900" fill="#996124">SNACK</text>
      <path d="M15 31 L24 35 M85 31 L76 35" stroke="#fff0bc" stroke-width="2"/>
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
const sink = document.getElementById("sink");
const instruction = document.getElementById("instruction");
const overlay = document.getElementById("result-overlay");
const resultText = document.getElementById("result-text");
const resultSub = document.getElementById("result-sub");

let currentTrash = null;
let cleaned = false;
let gameOver = false;
let dragOffsetX = 0;
let dragOffsetY = 0;
let pointerDragging = false;
let resultTimer = null;

// 각 쓰레기의 정답 쓰레기통
const trashTypes = [
    { id: "juice", answer: "yellow", name: "오렌지 주스 페트병" },
    { id: "cola", answer: "green", name: "콜라 캔" },
    { id: "bag", answer: "red", name: "과자 봉지" }
];

// ==========================================
// 5. 화면 전환과 게임 시작
// ==========================================

function showStartScreen() {
    clearTimeout(resultTimer);
    overlay.classList.remove("show");
    gameScreen.classList.remove("active");
    startScreen.classList.add("active");
    gameOver = false;
}

function startGame() {
    clearTimeout(resultTimer);
    overlay.classList.remove("show");
    startScreen.classList.remove("active");
    gameScreen.classList.add("active");

    // 세 가지 쓰레기 중 하나를 무작위로 선택해요.
    currentTrash = trashTypes[
        Math.floor(Math.random() * trashTypes.length)
    ];

    cleaned = false;
    gameOver = false;

    trash.innerHTML = pictures[currentTrash.id];
    trash.classList.remove("bag-glow", "dragging");
    trash.style.left = "50%";
    trash.style.top = "43%";
    trash.style.transform = "translate(-50%, -50%)";
    trash.style.display = "flex";
    trash.setAttribute("draggable", "true");

    instruction.innerHTML =
        "🧽 먼저 <b>쓰레기를 싱크대</b>에 드래그해 주세요.";
}

// ==========================================
// 6. 성공 / 실패 처리
//    결과를 3초 동안 보여준 뒤 첫 화면으로 돌아가요.
// ==========================================

function finishGame(success) {
    if (gameOver) return;
    gameOver = true;

    resultText.textContent = success ? "성공! 🎉" : "실패! 😢";
    resultText.style.color = success ? "#3aab72" : "#e65f5f";
    resultSub.textContent = success
        ? "분리배출을 잘했어요!"
        : "다시 도전해 봐요!";
    overlay.classList.add("show");

    resultTimer = setTimeout(() => {
        showStartScreen();
    }, 3000);
}

// ==========================================
// 7. 드래그 도우미
//    마우스와 터치 모두 사용할 수 있게 해요.
// ==========================================

function placeTrashAt(clientX, clientY) {
    const rect = stage.getBoundingClientRect();

    // 드래그한 위치를 게임 무대 안의 좌표로 바꿔요.
    let x = clientX - rect.left - dragOffsetX;
    let y = clientY - rect.top - dragOffsetY;

    x = Math.max(0, Math.min(rect.width - trash.offsetWidth, x));
    y = Math.max(0, Math.min(rect.height - trash.offsetHeight, y));

    trash.style.left = x + "px";
    trash.style.top = y + "px";
    trash.style.transform = "none";
}

function getDropZone(clientX, clientY) {
    // 마우스를 놓은 위치에 있는 싱크대 또는 쓰레기통을 찾아요.
    const element = document.elementFromPoint(clientX, clientY);
    if (!element) return null;

    const zone = element.closest("[data-zone]");
    if (!zone || !stage.contains(zone)) return null;

    return zone.dataset.zone;
}

function handleDrop(zone) {
    if (gameOver || !currentTrash) return;

    // 싱크대를 먼저 거치지 않았다면 쓰레기통에 바로 넣을 수 없어요.
    if (!cleaned) {
        if (zone === "sink") {
            cleaned = true;

            if (currentTrash.id === "juice") {
                trash.innerHTML = pictures.emptyBottle;
                instruction.innerHTML =
                    "✨ 주스를 비웠어요! 빈 페트병을 <b>노란색 플라스틱 통</b>에 넣어요.";
            } else if (currentTrash.id === "cola") {
                trash.innerHTML = pictures.plainCan;
                instruction.innerHTML =
                    "✨ 캔을 깨끗하게 정리했어요! <b>초록색 캔·고철 통</b>으로 옮겨요.";
            } else {
                trash.classList.add("bag-glow");
                instruction.innerHTML =
                    "✨ 반짝반짝! 과자 봉지는 <b>빨간색 비닐 통</b>으로 옮겨요.";
            }

            // 쓰레기를 싱크대 중앙에 놓아 다시 드래그할 수 있게 해요.
            trash.style.left = "50%";
            trash.style.top = "43%";
            trash.style.transform = "translate(-50%, -50%)";
        } else if (zone === "red" || zone === "yellow" || zone === "green") {
            finishGame(false);
        }

        return;
    }

    // 싱크대를 거친 다음에는 올바른 쓰레기통인지 확인해요.
    if (zone === "red" || zone === "yellow" || zone === "green") {
        finishGame(zone === currentTrash.answer);
    } else if (zone === "sink") {
        // 싱크대에 다시 놓아도 정리된 상태를 유지해요.
        trash.style.left = "50%";
        trash.style.top = "43%";
        trash.style.transform = "translate(-50%, -50%)";
    }
}

// ==========================================
// 8. HTML 드래그 앤 드롭 이벤트
// ==========================================

trash.addEventListener("dragstart", (event) => {
    if (gameOver) {
        event.preventDefault();
        return;
    }

    // 브라우저 기본 드래그 이미지 대신 현재 쓰레기를 사용해요.
    event.dataTransfer.setData("text/plain", "trash");
    event.dataTransfer.effectAllowed = "move";
    trash.classList.add("dragging");
});

trash.addEventListener("dragend", (event) => {
    trash.classList.remove("dragging");

    const zone = getDropZone(event.clientX, event.clientY);
    if (zone) {
        handleDrop(zone);
    }
});

document.querySelectorAll("[data-zone]").forEach((zoneElement) => {
    zoneElement.addEventListener("dragover", (event) => {
        event.preventDefault();
        zoneElement.classList.add("drag-over");
    });

    zoneElement.addEventListener("dragleave", () => {
        zoneElement.classList.remove("drag-over");
    });

    zoneElement.addEventListener("drop", (event) => {
        event.preventDefault();
        document.querySelectorAll("[data-zone]").forEach((el) => {
            el.classList.remove("drag-over");
        });

        // 일부 브라우저에서는 dragend에서도 처리되므로
        // drop에서는 중복 판정을 하지 않아요.
    });
});

// ==========================================
// 9. 마우스와 터치로 직접 드래그하기
//    화면에서 쓰레기를 직접 잡아 이동할 수 있어요.
// ==========================================

trash.addEventListener("pointerdown", (event) => {
    if (gameOver) return;

    // 브라우저의 기본 이미지 드래그와 중복되지 않게 해요.
    event.preventDefault();

    pointerDragging = true;
    trash.classList.add("dragging");

    const trashRect = trash.getBoundingClientRect();
    dragOffsetX = event.clientX - trashRect.left;
    dragOffsetY = event.clientY - trashRect.top;

    trash.setPointerCapture(event.pointerId);
});

trash.addEventListener("pointermove", (event) => {
    if (!pointerDragging || gameOver) return;

    const rect = stage.getBoundingClientRect();
    let x = event.clientX - rect.left - dragOffsetX;
    let y = event.clientY - rect.top - dragOffsetY;

    x = Math.max(0, Math.min(rect.width - trash.offsetWidth, x));
    y = Math.max(0, Math.min(rect.height - trash.offsetHeight, y));

    trash.style.left = x + "px";
    trash.style.top = y + "px";
    trash.style.transform = "none";

    // 현재 쓰레기 위치에 따라 드롭할 장소를 강조해요.
    document.querySelectorAll("[data-zone]").forEach((el) => {
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

trash.addEventListener("pointerup", (event) => {
    if (!pointerDragging) return;

    pointerDragging = false;
    trash.classList.remove("dragging");

    document.querySelectorAll("[data-zone]").forEach((el) => {
        el.classList.remove("drag-over");
    });

    const zone = getDropZone(event.clientX, event.clientY);
    if (zone) {
        handleDrop(zone);
    }
});

trash.addEventListener("pointercancel", () => {
    pointerDragging = false;
    trash.classList.remove("dragging");
    document.querySelectorAll("[data-zone]").forEach((el) => {
        el.classList.remove("drag-over");
    });
});

// ==========================================
// 10. 버튼 이벤트
// ==========================================

startButton.addEventListener("click", startGame);
homeButton.addEventListener("click", showStartScreen);

// 처음에는 시작 화면만 보여줘요.
showStartScreen();
</script>
</body>
</html>
"""

# ==========================================
# 11. Streamlit 안에 게임 표시
# ==========================================
components.html(
    game_html,
    height=790,
    scrolling=True,
)
