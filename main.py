
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="알록달록 쓰레기 분류 게임",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: #fff8e9;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. 게임 HTML, CSS, JavaScript
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
    font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
    color: #654b38;
    background: #fff8e9;
    user-select: none;
    -webkit-user-select: none;
}

button {
    font-family: inherit;
    cursor: pointer;
}

#app {
    width: 100%;
    min-height: 780px;
    background: linear-gradient(180deg, #fff9ee, #ffefd5);
    position: relative;
    overflow: hidden;
}

.screen {
    display: none;
    min-height: 780px;
    padding: 20px 14px;
    align-items: center;
    flex-direction: column;
}

.screen.active {
    display: flex;
}

.game-title {
    text-align: center;
    color: #80583e;
    font-size: clamp(25px, 4vw, 37px);
    font-weight: 900;
    margin: 12px 0;
}

.subtitle {
    text-align: center;
    color: #a18165;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 18px;
}

/* 첫 화면 쓰레기통 */
.intro-bins {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: clamp(12px, 4vw, 35px);
    width: 100%;
    margin: 32px auto;
}

.bin {
    width: clamp(88px, 22vw, 150px);
    height: clamp(130px, 27vw, 185px);
    border: 4px solid rgba(255,255,255,.75);
    border-radius: 15px 15px 23px 23px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    color: white;
    font-weight: 900;
    font-size: clamp(16px, 3vw, 23px);
    line-height: 1.5;
    text-align: center;
    box-shadow: 0 8px 0 rgba(100,70,40,.12);
}

.bin::before {
    content: "";
    position: absolute;
    top: -12px;
    left: -6px;
    right: -6px;
    height: 16px;
    border: 3px solid rgba(255,255,255,.75);
    border-radius: 8px;
    background: inherit;
}

.red { background: #ee6262; }
.yellow { background: #efb92f; }
.green { background: #55ae79; }

.bin-emoji {
    font-size: 34px;
    margin-bottom: 6px;
}

.start-button {
    border: 0;
    border-radius: 40px;
    padding: 17px 48px;
    color: white;
    background: #ff9955;
    box-shadow: 0 6px 0 #d97a3d;
    font-size: 22px;
    font-weight: 900;
}

.start-button:hover {
    filter: brightness(1.04);
    transform: translateY(-2px);
}

.tip {
    text-align: center;
    margin-top: 25px;
    font-size: 14px;
    line-height: 1.7;
    color: #a18165;
}

/* 게임 화면 상단 */
.top-row {
    width: min(100%, 900px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.back-button {
    background: #fffdf8;
    color: #88674e;
    border: 2px solid #ead8bf;
    border-radius: 30px;
    padding: 10px 15px;
    font-size: 14px;
    font-weight: bold;
}

.step-label {
    background: white;
    border: 2px solid #f0dfc6;
    border-radius: 30px;
    padding: 9px 13px;
    font-size: 13px;
    font-weight: bold;
    color: #98734e;
}

.instruction {
    width: min(100%, 600px);
    text-align: center;
    background: white;
    border: 2px solid #f0dfc6;
    border-radius: 16px;
    padding: 12px;
    margin: 8px 0 14px;
    font-size: 15px;
    line-height: 1.6;
}

/* 게임 무대 */
#stage {
    position: relative;
    width: min(100%, 920px);
    height: 490px;
    flex-shrink: 0;
    overflow: hidden;
    border: 4px solid #f0d9b9;
    border-radius: 23px;
    background:
        linear-gradient(
            to bottom,
            #fff9ed 0%,
            #fff4df 72%,
            #e9cda7 72%,
            #e9cda7 100%
        );
    box-shadow: inset 0 -5px 0 rgba(151,108,65,.08);
}

/* 창문과 선반 */
.wall-window {
    position: absolute;
    top: 20px;
    right: 25px;
    width: 75px;
    height: 68px;
    border: 6px solid #e4c59e;
    border-radius: 8px;
    background: linear-gradient(135deg, #bce8e5, #e4f7e9);
    pointer-events: none;
}

.wall-window::before {
    content: "";
    position: absolute;
    left: 50%;
    height: 100%;
    width: 4px;
    background: #e4c59e;
}

.wall-window::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 100%;
    height: 4px;
    background: #e4c59e;
}

.wall-shelf {
    position: absolute;
    top: 112px;
    right: 16px;
    width: 100px;
    height: 8px;
    border-radius: 5px;
    background: #d3ad80;
    pointer-events: none;
}

/* 왼쪽 싱크대 */
#sink {
    position: absolute;
    left: 18%;
    top: 40%;
    transform: translate(-50%, -50%);
    width: clamp(130px, 21%, 190px);
    height: 130px;
    border-radius: 14px 14px 20px 20px;
    background: #b9dce0;
    border: 7px solid #8fb9c0;
    box-shadow: 0 8px 0 rgba(91,143,151,.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #477a83;
    font-weight: 900;
    z-index: 2;
    transition: background .15s, box-shadow .15s;
}

.sink-icon {
    font-size: 34px;
    line-height: 1.3;
}

.sink-label {
    font-size: 18px;
    margin-top: 3px;
}

#sink.drag-over {
    background: #d5f6f5;
    border-color: #42b9c5;
    box-shadow: 0 0 0 7px rgba(93,214,222,.25);
}

/* 쓰레기통 */
.stage-bin {
    position: absolute;
    bottom: 18px;
    width: 26%;
    max-width: 170px;
    height: 105px;
    border-radius: 12px 12px 18px 18px;
    border: 4px solid rgba(255,255,255,.72);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
    text-align: center;
    font-weight: 900;
    font-size: clamp(13px, 2vw, 17px);
    line-height: 1.35;
    box-shadow: 0 6px 0 rgba(90,65,43,.14);
    z-index: 2;
    transition: transform .15s, outline .15s;
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

#bin-red { left: 2%; }
#bin-yellow { left: 37%; }
#bin-green { right: 2%; }

.stage-bin .bin-emoji {
    font-size: 26px;
    margin-bottom: 0;
}

.stage-bin.drag-over {
    outline: 5px solid white;
    transform: translateY(-5px);
}

/* 드래그할 쓰레기 */
#trash {
    position: absolute;
    left: 63%;
    top: 37%;
    width: 100px;
    height: 125px;
    z-index: 10;
    cursor: grab;
    touch-action: none;
    -webkit-user-select: none;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
}

#trash.dragging {
    cursor: grabbing;
    filter: drop-shadow(0 9px 7px rgba(0,0,0,.2));
    z-index: 30;
}

.trash-svg {
    width: 100%;
    height: 100%;
    overflow: visible;
    pointer-events: none;
}

/* 과자 봉지 반짝임 */
#trash.bag-glow {
    animation: sparkle 0.8s infinite alternate;
}

@keyframes sparkle {
    from {
        filter: drop-shadow(0 0 5px #75eaff)
                drop-shadow(0 0 12px #53dfff);
    }
    to {
        filter: drop-shadow(0 0 13px #75eaff)
                drop-shadow(0 0 24px #53dfff)
                drop-shadow(0 0 34px #a2f5ff);
    }
}

/* 성공/실패 화면 */
#result-overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: rgba(255,248,233,.94);
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
    font-size: clamp(50px, 10vw, 82px);
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
    color: #a18469;
    font-size: 13px;
    margin-top: 12px;
}

@media (max-width: 520px) {
    #app, .screen { min-height: 730px; }
    #stage { height: 450px; }
    #sink {
        left: 22%;
        top: 38%;
        width: 125px;
        height: 112px;
    }
    #trash {
        width: 78px;
        height: 105px;
    }
    .stage-bin {
        width: 30%;
        height: 92px;
        bottom: 15px;
    }
    #bin-red { left: 1%; }
    #bin-yellow { left: 35%; }
    #bin-green { right: 1%; }
    .wall-window { width: 55px; height: 52px; }
    .wall-shelf { top: 91px; width: 72px; }
    .instruction { font-size: 13px; }
}
</style>
</head>

<body>
<div id="app">

    <!-- 시작 화면 -->
    <section id="start-screen" class="screen active">
        <div style="font-size:48px; margin-top:20px;">♻️</div>
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

        <button id="start-button" class="start-button">
            시작하기 ✨
        </button>

        <p class="tip">
            💡 쓰레기를 먼저 싱크대에 놓은 다음<br>
            알맞은 쓰레기통으로 옮겨 주세요!
        </p>
    </section>

    <!-- 실제 게임 화면 -->
    <section id="game-screen" class="screen">
        <div class="top-row">
            <button id="home-button" class="back-button">← 처음으로</button>
            <span class="step-label">미션: 쓰레기 분리배출</span>
        </div>

        <h1 class="game-title">어디에 버려야 할까요?</h1>

        <p class="subtitle" style="margin-bottom:5px;">
            쓰레기를 잡고 드래그해서 이동해 보세요!
        </p>

        <div id="instruction" class="instruction">
            🧽 먼저 쓰레기를 싱크대에 드래그해 주세요.
        </div>

        <div id="stage">
            <div class="wall-window"></div>
            <div class="wall-shelf"></div>

            <!-- 싱크대: 왼쪽 -->
            <div id="sink" data-zone="sink">
                <div class="sink-icon">🚰</div>
                <div class="sink-label">싱크대</div>
            </div>

            <!-- 아래쪽 쓰레기통 -->
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

            <!-- 현재 쓰레기가 나타나는 자리 -->
            <div id="trash"></div>
        </div>

        <p class="bottom-note">
            🧡 작은 실천이 지구를 웃게 만들어요!
        </p>
    </section>

    <!-- 성공 또는 실패 메시지 -->
    <div id="result-overlay">
        <div id="result-text">성공! 🎉</div>
        <div id="result-sub">분리배출을 잘했어요!</div>
    </div>
</div>

<script>
// ==========================================
// 3. 쓰레기 일러스트
//    외부 이미지 파일 없이 SVG로 그려요.
// ==========================================

const pictures = {
    juice: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <rect x="39" y="5" width="22" height="13" rx="3" fill="#579447"/>
      <path d="M38 17 L62 17 L62 30 Q70 37 72 47 L75 104 Q75 115 64 116 L36 116 Q25 115 25 104 L28 47 Q30 37 38 30 Z"
        fill="#ffad42" stroke="#d88a29" stroke-width="2"/>
      <path d="M34 45 Q32 58 33 73" fill="none" stroke="#ffe6ac" stroke-width="5" stroke-linecap="round"/>
      <rect x="28" y="60" width="44" height="30" rx="5" fill="#fff2c9"/>
      <circle cx="50" cy="75" r="10" fill="#ff9c25"/>
      <path d="M50 65 L50 85 M40 75 L60 75 M43 68 L57 82 M57 68 L43 82"
        stroke="#ffe5a3" stroke-width="1.5"/>
      <text x="50" y="99" text-anchor="middle" font-size="7" fill="#a95d20" font-weight="bold">ORANGE</text>
    </svg>`,

    emptyBottle: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <rect x="40" y="5" width="20" height="12" rx="3" fill="#78b875"/>
      <path d="M39 17 L61 17 L61 30 Q69 38 71 47 L74 103 Q75 115 64 116 L36 116 Q25 115 26 103 L29 47 Q31 38 39 30 Z"
        fill="#d8f2ed" fill-opacity=".8" stroke="#77b9ad" stroke-width="2.5"/>
      <path d="M35 43 Q32 62 35 95" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
      <path d="M33 35 L67 35 M31 43 L69 43" stroke="#a5d7cc" stroke-width="2"/>
      <path d="M36 103 L64 103" stroke="#a5d7cc" stroke-width="2"/>
    </svg>`,

    cola: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <path d="M25 18 Q23 22 24 28 L28 105 Q29 113 37 115 L63 115 Q71 113 72 105 L76 28 Q77 22 75 18 Z"
        fill="#d72e39" stroke="#a9212d" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="24" ry="6" fill="#eee" stroke="#aaa" stroke-width="1.5"/>
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
        fill="url(#metal)" stroke="#84979e" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="23" ry="7" fill="#e8eded" stroke="#84979e" stroke-width="2"/>
      <ellipse cx="50" cy="19" rx="10" ry="3" fill="#9eacb0"/>
      <path d="M32 33 L35 98" stroke="#fff" stroke-width="4" opacity=".85"/>
      <path d="M30 105 Q50 111 70 105" stroke="#87989d" stroke-width="2" fill="none"/>
    </svg>`,

    bag: `
    <svg class="trash-svg" viewBox="0 0 100 125">
      <path d="M20 20 L80 20 L85 31 L81 101 L73 110 L27 110 L19 101 L15 31 Z"
        fill="#f4bd52" stroke="#d99b31" stroke-width="2.5"/>
      <path d="M20 20 L80 20 L76 29 L24 29 Z" fill="#ffe5a0"/>
      <path d="M19 100 L81 100 L73 110 L27 110 Z" fill="#e6a73d"/>
      <rect x="23" y="41" width="54" height="43" rx="8" fill="#fff4d5"/>
      <circle cx="50" cy="61" r="13" fill="#ee7c45"/>
      <circle cx="45" cy="57" r="2" fill="#fff1c4"/>
      <circle cx="55" cy="57" r="2" fill="#fff1c4"/>
      <path d="M45 66 Q50 71 55 66" stroke="#fff1c4" stroke-width="2" fill="none" stroke-linecap="round"/>
      <text x="50" y="95" text-anchor="middle" font-size="8" font-weight="900" fill="#996124">SNACK</text>
    </svg>`
};

// ==========================================
// 4. 화면 요소와 게임 상태
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

// 각 쓰레기의 정답
const trashTypes = [
    { id: "juice", answer: "yellow" },
    { id: "cola", answer: "green" },
    { id: "bag", answer: "red" }
];

// ==========================================
// 5. 게임 시작과 첫 화면 복귀
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

    // 쓰레기 세 종류 중 하나를 무작위로 선택해요.
    currentTrash = trashTypes[
        Math.floor(Math.random() * trashTypes.length)
    ];

    cleaned = false;
    gameOver = false;
    dragging = false;

    trash.innerHTML = pictures[currentTrash.id];
    trash.classList.remove("bag-glow", "dragging");
    trash.style.display = "flex";
    trash.style.left = "63%";
    trash.style.top = "37%";
    trash.style.transform = "translate(-50%, -50%)";
    trash.style.visibility = "visible";

    instruction.innerHTML =
        "🧽 먼저 쓰레기를 <b>왼쪽 싱크대</b>에 드래그해 주세요.";
}

// ==========================================
// 6. 결과 표시
// ==========================================

function finishGame(success) {
    if (gameOver) return;

    gameOver = true;
    dragging = false;

    resultText.textContent = success ? "성공! 🎉" : "실패! 😢";
    resultText.style.color = success ? "#36a66f" : "#e65f5f";
    resultSub.textContent = success
        ? "분리배출을 잘했어요!"
        : "다시 도전해 봐요!";

    overlay.classList.add("show");

    // 3초 뒤에 첫 화면으로 돌아가요.
    resultTimer = setTimeout(showStartScreen, 3000);
}

// ==========================================
// 7. 드롭 위치 판정
//    쓰레기 그림을 잠시 숨겨 밑의 영역을 확인해요.
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
// 8. 싱크대와 쓰레기통에 놓았을 때
// ==========================================

function handleDrop(zone) {
    if (gameOver || !currentTrash || !zone) return;

    // 아직 싱크대를 거치지 않은 경우
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
                    "✨ 라벨을 제거했어요! 일반 캔을 <b>초록색 캔·고철 통</b>에 넣어요.";
            } else {
                trash.classList.add("bag-glow");
                instruction.innerHTML =
                    "✨ 반짝반짝! 과자 봉지를 <b>빨간색 비닐 통</b>에 넣어요.";
            }

            // 처리 후 쓰레기를 중앙에 놓아 다시 잡기 쉽게 해요.
            trash.style.left = "55%";
            trash.style.top = "37%";
            trash.style.transform = "translate(-50%, -50%)";
        } else {
            // 싱크대보다 쓰레기통을 먼저 선택하면 실패예요.
            finishGame(false);
        }

        return;
    }

    // 싱크대를 거친 뒤 정답을 판정해요.
    if (
        zone === "red" ||
        zone === "yellow" ||
        zone === "green"
    ) {
        finishGame(zone === currentTrash.answer);
    } else if (zone === "sink") {
        // 싱크대에 다시 놓아도 정리된 상태를 유지해요.
        trash.style.left = "55%";
        trash.style.top = "37%";
        trash.style.transform = "translate(-50%, -50%)";
    }
}

// ==========================================
// 9. 마우스 및 터치 드래그
//    pointer 이벤트 하나로 마우스와 터치를 처리해요.
// ==========================================

trash.addEventListener("pointerdown", function(event) {
    if (gameOver || !currentTrash) return;

    event.preventDefault();

    dragging = true;
    trash.classList.add("dragging");

    const rect = trash.getBoundingClientRect();

    // 쓰레기 그림 안에서 잡은 지점을 기억해요.
    offsetX = event.clientX - rect.left;
    offsetY = event.clientY - rect.top;

    // 손가락이 쓰레기 밖으로 나가도 드래그를 이어 가요.
    try {
        trash.setPointerCapture(event.pointerId);
    } catch (error) {
        // 브라우저가 포인터 캡처를 지원하지 않아도 계속 진행해요.
    }
});

trash.addEventListener("pointermove", function(event) {
    if (!dragging || gameOver) return;

    event.preventDefault();

    const rect = stage.getBoundingClientRect();

    // 브라우저 화면 좌표를 게임 무대 좌표로 바꿔요.
    let x = event.clientX - rect.left - offsetX;
    let y = event.clientY - rect.top - offsetY;

    x = Math.max(0, Math.min(rect.width - trash.offsetWidth, x));
    y = Math.max(0, Math.min(rect.height - trash.offsetHeight, y));

    trash.style.left = x + "px";
    trash.style.top = y + "px";
    trash.style.transform = "none";

    // 현재 놓을 수 있는 영역을 강조해요.
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

    // 놓은 위치를 확인하고 게임을 진행해요.
    const zone = getDropZone(event.clientX, event.clientY);

    if (zone) {
        handleDrop(zone);
    } else {
        // 싱크대나 쓰레기통이 아닌 곳이면 원래 위치로 돌려요.
        trash.style.left = "63%";
        trash.style.top = "37%";
        trash.style.transform = "translate(-50%, -50%)";
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

// 첫 화면부터 시작해요.
showStartScreen();
</script>
</body>
</html>
"""

# ==========================================
# 3. Streamlit 화면에 게임 표시
# ==========================================
components.html(
    game_html,
    height=800,
    scrolling=True,
)
