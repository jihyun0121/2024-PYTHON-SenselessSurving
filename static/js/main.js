const storyText = document.getElementById('story-text');
const choicesDiv = document.getElementById('choices');
const statusDiv = document.getElementById('status');
const resetButton = document.getElementById('reset-button');

// 초기 상태 설정
let lives = 3;
let mental = 3;
let money = 3;
let gameOver = false;
let currentStory;
let foundTreasures = 0;

// 사용된 스토리 추적을 위한 배열
let usedStories = [];
let requiredStorySeen = false; // 후속 스토리가 나오기 위한 플래그

// 스토리 데이터
const stories = [
    {   // 어두운 숲 1 스토리
        start: {
            text: "어두운 숲 1",
            image: "/static/image/임시 이미지.svg",
            choices: [
                { text: "북쪽", next: "north_path" },
                { text: "남쪽", next: "south_path" }
            ]
        },
        north_path: {
            text: "보물 발견 1",
            choices: [
                { text: "열기", next: "treasure" },
                { text: "그냥 두기", next: "leave_chest" }
            ]
        },
        south_path: {
            text: "야생 동물 조우 1",
            choices: [
                { text: "싸우기", next: "fight_animal" },
                { text: "도망가기", next: "run_away" }
            ]
        },
        treasure: {
            text: "보물 획득",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        leave_chest: {
            text: "떠나기, 야생동물 조우 2",
            choices: [
                { text: "싸우기", next: "fight_animal" },
                { text: "도망가기", next: "run_away" }
            ]
        },
        fight_animal: {
            text: "부상, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        run_away: {
            text: "도망, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        next_story: {
            text: "다음으로",
            choices: [
                { text: "다음", next: "start"}
            ]
        }
    },
    {   // 오래된 성 스토리
        start: {
            text: "오래된 성",
            image: "/static/image/임시 이미지.svg",
            choices: [
                { text: "들어가기", next: "enter_castle" },
                { text: "주변 탐험", next: "explore_area" }
            ]
        },
        enter_castle: {
            text: "고대 유물 발견 1",
            choices: [
                { text: "유물 조사", next: "inspect_relic" },
                { text: "유물 무시", next: "ignore_relic" }
            ]
        },
        explore_area: {
            text: "탐험, 덫 걸림",
            choices: [
                { text: "벗어나기", next: "escape_trap" },
                { text: "도움 요청", next: "call_for_help" }
            ]
        },
        inspect_relic: {
            text: "유물 조사, 보물발견 2",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        ignore_relic: {
            text: "유물 무시, 덫 걸림.",
            choices: [
                { text: "덫에서 벗어납니다", next: "escape_trap" },
                { text: "도움을 요청합니다", next: "call_for_help" }
            ]
        },
        escape_trap: {
            text: "부상, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        call_for_help: {
            text: "도움 요청, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        next_story: {
            text: "다음으로",
            choices: [
                { text: "다음", next: "start"}
            ]
        }
    },
    {   // 신비한 동굴
        start: {
            text: "신비로운 동굴 발견",
            image: "/static/image/임시 이미지.svg",
            choices: [
                { text: "들어가기", next: "enter_cave" },
                { text: "지나기기", next: "pass_cave" }
            ]
        },
        enter_cave: {
            text: "보석 발견",
            choices: [
                { text: "줍기", next: "take_gem" },
                { text: "무시하기", next: "ignore_gem" }
            ]
        },
        pass_cave: {
            text: "지나침, 멘탈 감소",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        take_gem: {
            text: "보석 획득, 돈 회복",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        ignore_gem: {
            text: "보석 무시",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        next_story: {
            text: "다음으로",
            choices: [
                { text: "다음", next: "start"}
            ]
        },
        isFollowUp: false
    },
    {   // 신비한 동굴 후속 스토리
        start: {
            text: "갈림길",
            image: "/static/image/임시 이미지.svg",
            choices: [
                { text: "북쪽", next: "north_path" },
                { text: "남쪽", next: "south_path" }
            ]
        },
        north_path: {
            text: "북쪽, 동굴 발견",
            choices: [
                { text: "들어가기", next: "enter_cave" },
                { text: "지나치기", next: "pass_cave" }
            ]
        },
        south_path: {
            text: "남쪽, 야생 동물 조우",
            choices: [
                { text: "싸우기", next: "fight_animal" },
                { text: "도망", next: "run_away" }
            ]
        },
        enter_cave: {
            text: "고대 유물 발견 2",
            choices: [
                { text: "유물 조사", next: "inspect_relic" },
                { text: "유물 무시", next: "ignore_relic" }
            ]
        },
        inspect_relic: {
            text: "유물 조사, 보물발견 3",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        ignore_relic: {
            text: "유물 무시, 덫 걸림.",
            choices: [
                { text: "덫에서 벗어납니다", next: "escape_trap" },
                { text: "도움을 요청합니다", next: "call_for_help" }
            ]
        },
        escape_trap: {
            text: "부상, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        call_for_help: {
            text: "도움 요청, 목숨 감소",
            choices: [
                { text: "다음", next: "next_story" }
            ]
        },
        next_story: {
            text: "다음으로",
            choices: [
                { text: "다음", next: "start"}
            ]
        },
        requiresPrevious: true,
        isFollowUp: true
    },
    {   // 어두운 숲 2 스토리
        start: {
            text: "어두운 숲2",
            image: "/static/image/임시 이미지.svg",
            choices: [
                { text: "나아가기", next: "follow_path" },
                { text: "탐색하기", next: "explore_forest" }
            ]
        },
        follow_path: {
            text: "은화 주머니 발견",
            choices: [
                { text: "열어보기", next: "gain_money" },
                { text: "지나가기", next: "leave_pouch" }
            ]
        },
        explore_forest: {
            text: "길 잃기, 멘탈 감소",
            choices: [
                { text: "정신 차리기", next: "gain_mental" },
                { text: "포기", next: "lose_mental" }
            ]
        },
        gain_money: {
            text: "돈 회복",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        leave_pouch: {
            text: "아무것도 없음",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        gain_mental: {
            text: "멘탈 회복",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        lose_mental: {
            text: "멘탈 감소",
            choices: [
                { text: "계속", next: "next_story" }
            ]
        },
        next_story: {
            text: "다음으로",
            choices: [
                { text: "다음", next: "start"}
            ]
        }
    }//,
    // {   //섬 스토리
    //     start: {
    //         text: "섬에 갇힘",
    //         image: "/static/image/임시 이미지.svg",
    //         choices: [
    //             { text: "탐험하기", next: "explore_island" },
    //             { text: "구조 기다리기", next: "wait_for_rescue" }
    //         ]
    //     },
    //     explore_island: {
    //         text: "유적 발견",
    //         choices: [
    //             { text: "유적 조사", next: "explore_ruins" },
    //             { text: "다른 곳 탐험하기", next: "explore_another_place" }
    //         ]
    //     },
    //     wait_for_rescue: {
    //         text: "구조 반응 없음",
    //         choices: [
    //             { text: "섬 탐험하기", next: "explore_island" },
    //             { text: "기다리기", next: "wait_longer" }
    //         ]
    //     },
    //     explore_ruins: {
    //         text: "보물 발견",
    //         choices: [
    //             { text: "계속합니다", next: "next_story" }
    //         ]
    //     },
    //     explore_another_place: {
    //         text: "아무것도 없음",
    //         choices: [
    //             { text: "계속합니다", next: "explore_island" }
    //         ]
    //     },
    //     wait_longer: {
    //         text: "여전히 구조 반응 없음",
    //         choices: [
    //             { text: "섬을 탐험합니다", next: "explore_island" },
    //             { text: "기다립니다", next: "wait_longer" }
    //         ]
    //     },
    //     next_story: {
    //         text: "다음으로",
    //         choices: [
    //             { text: "다음", next: "start"}
    //         ]
    //     },
    //     isFollowUp: false,
    //     key: "island_story"
    // },
    // {   // 섬 후속 스토리
    //     start: {
    //         text: "마을 축제",
    //         image: "/static/image/임시 이미지.svg",
    //         choices: [
    //             { text: "참여하기", next: "join_festival" },
    //             { text: "무시하기", next: "ignore_festival" }
    //         ]
    //     },
    //     join_festival: {
    //         text: "정보와 새로운 친구",
    //         choices: [
    //             { text: "계속", next: "next_story" }
    //         ]
    //     },
    //     ignore_festival: {
    //         text: "무시하고 탐험 계속",
    //         choices: [
    //             { text: "계속", next: "next_story" }
    //         ]
    //     },
    //     next_story: {
    //         text: "다음으로",
    //         choices: [
    //             { text: "다음", next: "start"}
    //         ]
    //     },
    //     isFollowUp: true,
    //     key: "follow_up_story"
    // }

];

// 게임 시작 함수
function startGame() {
    // 초기화
    lives = 3;
    mental = 3;
    money = 3;
    gameOver = false;
    foundTreasures = 0;
    usedStories = [];
    requiredStorySeen = false;

    // 게임 시작 후 초기 스토리 표시
    selectNewStory();
    displayStory('start');
    updateStatus();
}

// 새로운 스토리 선택 함수
function selectNewStory() {
    if (usedStories.length === stories.length) {
        endGame();
    }
    
    let availableStories = stories.filter((_, index) => !usedStories.includes(index));
    
    // 후속 스토리는 이전 스토리가 나오기 전에는 선택되지 않도록 필터링
    if (!requiredStorySeen) {
        availableStories = availableStories.filter((story) => !story.isFollowUp);
    }
    
    let randomIndex = Math.floor(Math.random() * availableStories.length);
    currentStory = availableStories[randomIndex];
    usedStories.push(stories.indexOf(currentStory));
    
    // 후속 스토리가 선택된 경우, 플래그를 true로 설정
    if (currentStory.requiresPrevious) {
        requiredStorySeen = true;
    }
}

// 타이핑 애니메이션 함수
function typeWriterEffect(text) {
    const textElement = document.getElementById('story-text-content');
    textElement.innerHTML = '';
    let i = 0;
    const speed = 50; // 타이핑 속도

    function typeWriter() {
        if (i < text.length) {
            textElement.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }

    typeWriter();
}

// 스토리 표시 함수
function displayStory(storyKey) {
    const scene = currentStory[storyKey];
    
    // 이미지가 있을 경우 이미지를 표시
    let imageHtml = '';
    if (scene.image) {
        imageHtml = `<img src="${scene.image}" alt="story image" />`;
    }

    // 스토리 텍스트는 타이핑 애니메이션으로 표시
    storyText.innerHTML = `${imageHtml}<p id="story-text-content"></p>`;
    typeWriterEffect(scene.text);

    choicesDiv.innerHTML = '';

    scene.choices.forEach(choice => {
        const button = document.createElement('button');
        button.textContent = choice.text;
        button.addEventListener('click', () => makeChoice(choice.next));
        choicesDiv.appendChild(button);
    });
}


// 선택지 선택 함수
function makeChoice(next) {
    displayStory(next);
    switch (next) {
        case 'treasure':
        case 'inspect_relic':
        case 'explore_ruins':
            foundTreasures++;
            if (foundTreasures >= 2) {
                endGame('win');
            } else {
                displayStory(next);
            }
            break;
        case 'fight_animal':
        case 'run_away':
        case 'escape_trap':
        case 'call_for_help':
            lives--;
            if (lives <= 0) {
                endGame('lose');
            } else {
                updateStatus();
                displayStory(next);
            }
            break;
        case 'explore_forest':
        case 'pass_cave':
            mental--;
            if (mental <= 0) {
                endGame('lose');
            } else {
                updateStatus();
                displayStory(next);
            }
            break;
        case 'gain_money':
            money++;
            updateStatus();
            displayStory(next);
            break;
        case 'gain_mental':
            mental++;
            updateStatus();
            displayStory(next);
            break;
        case 'next_story':
            selectNewStory();
            displayStory('start');
            break;
        default:
            displayStory(next);
            break;
    }
    updateStatus();
}

// 게임 종료 함수
function endGame(result) {
    gameOver = true;
    if (result === 'win') {
        storyText.textContent = `축하합니다! 보물을 모두 찾았습니다! 게임에 이겼습니다!`;
    } else if(usedStories.length === stories.length) {
        storyText.textContent = `탐험을 완료하였습니다`;
    } else if(lives == 0) {
        storyText.textContent = `모든 목숨을 잃었습니다. 게임 오버!`;
    } else if(mental == 0) {
        storyText.textContent = `모든 목숨을 잃었습니다. 게임 오버!`;
    }
    choicesDiv.innerHTML = '<button id="restart-button">게임 다시 시작</button>';
    updateStatus();
    document.getElementById('restart-button').addEventListener('click', startGame);
}

// 상태 업데이트 함수 (목숨, 멘탈, 돈)
function updateStatus() {
    const heartFull = '<img src="/static/image/체력.svg" />';
    const heartEmpty = '<img src="/static/image/체력 감소.svg" />';
    const brainFull = '<img src="/static/image/지능.svg" />';
    const brainEmpty = '<img src="/static/image/지능 감소.svg" />';
    const moneyFull = '<img src="/static/image/돈.svg" />';
    const moneyEmpty = '<img src="/static/image/돈 감소.svg" />';
    const treasureIcon = '✨';

    // 목숨 상태 업데이트
    let livesText = '';
    for (let i = 0; i < 3; i++) {
        if (i < lives) {
            livesText += heartFull;
        } else {
            livesText += heartEmpty;
        }
    }

    // 멘탈 상태 업데이트
    let mentalText = '';
    for (let i = 0; i < 3; i++) {
        if (i < mental) {
            mentalText += brainFull;
        } else {
            mentalText += brainEmpty;
        }
    }

    // 돈 상태 업데이트
    let moneyText = '';
    for (let i = 0; i < 3; i++) {
        if (i < money) {
            moneyText += moneyFull;
        } else {
            moneyText += moneyEmpty;
        }
    }

    // 찾은 보물 상태 업데이트
    let foundTreasureText = '';
    for (let i = 0; i < foundTreasures; i++) {
        foundTreasureText += treasureIcon;
    }

    // 상태 업데이트
    statusDiv.innerHTML = `
        <p>목숨: ${livesText}</p>
        <p>멘탈: ${mentalText}</p>
        <p>돈: ${moneyText}</p>
        <p>찾은 보물: ${foundTreasureText}</p>
    `;
}

resetButton.addEventListener('click', () => startGame());

// 페이지 로드 시 게임 시작
window.onload = startGame;