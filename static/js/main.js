const storyText = document.getElementById('story-text');
const choicesDiv = document.getElementById('choices');
const statusDiv = document.getElementById('status');
const resetButton = document.getElementById('reset-button');
const loadButton = document.getElementById('load-button'); // 불러오기 버튼

// 초기 상태 설정
let lives = 3;
let mental = 3;
let money = 3;
let gameOver = false;
let currentStory;
let foundTreasures = 0;
const totalTreasures = 2; // 보물의 총 개수

// 사용된 스토리 추적을 위한 배열
let usedStories = [];

// 스토리 데이터
const stories = [
    {
        start: {
            text: "어두운 숲에 왔습니다. 북쪽과 남쪽으로 갈 수 있는 길이 있습니다.",
            choices: [
                { text: "북쪽으로 갑니다", next: "north_path" },
                { text: "남쪽으로 갑니다", next: "south_path" }
            ]
        },
        north_path: {
            text: "보물 상자를 발견했습니다!",
            choices: [
                { text: "상자를 엽니다", next: "treasure" },
                { text: "그냥 두고 갑니다", next: "leave_chest" }
            ]
        },
        south_path: {
            text: "야생 동물을 만났습니다!",
            choices: [
                { text: "동물과 싸웁니다", next: "fight_animal" },
                { text: "도망갑니다", next: "run_away" }
            ]
        },
        treasure: {
            text: "보물을 찾았습니다! 축하합니다!",
            choices: []
        },
        leave_chest: {
            text: "상자를 두고 나왔습니다. 그러나 야생 동물에게 습격받았습니다!",
            choices: [
                { text: "동물과 싸웁니다", next: "fight_animal" },
                { text: "도망갑니다", next: "run_away" }
            ]
        },
        fight_animal: {
            text: "용감하게 싸웠지만 부상을 입었습니다. 목숨이 하나 줄었습니다.",
            choices: [
                { text: "계속합니다", next: "injured" }
            ]
        },
        run_away: {
            text: "도망쳤지만 목숨이 하나 줄었습니다.",
            choices: [
                { text: "계속합니다", next: "injured" }
            ]
        },
        injured: {
            text: "시작 지점으로 돌아왔습니다. 조심하세요!",
            choices: [
                { text: "북쪽으로 갑니다", next: "north_path" },
                { text: "남쪽으로 갑니다", next: "south_path" }
            ]
        }
    },
    {
        start: {
            text: "당신은 오래된 성 앞에 서 있습니다. 성문이 열려 있습니다.",
            choices: [
                { text: "성 안으로 들어갑니다", next: "enter_castle" },
                { text: "주변을 탐험합니다", next: "explore_area" }
            ]
        },
        enter_castle: {
            text: "성 안에 들어가니 고대 유물이 있습니다.",
            choices: [
                { text: "유물을 조사합니다", next: "inspect_relic" },
                { text: "유물을 무시합니다", next: "ignore_relic" }
            ]
        },
        explore_area: {
            text: "주변을 탐험하던 중 덫에 걸렸습니다.",
            choices: [
                { text: "덫에서 벗어납니다", next: "escape_trap" },
                { text: "도움을 요청합니다", next: "call_for_help" }
            ]
        },
        inspect_relic: {
            text: "유물을 조사하니 숨겨진 보물을 발견했습니다!",
            choices: []
        },
        ignore_relic: {
            text: "유물을 무시하고 지나갑니다. 그러자 덫에 걸렸습니다.",
            choices: [
                { text: "덫에서 벗어납니다", next: "escape_trap" },
                { text: "도움을 요청합니다", next: "call_for_help" }
            ]
        },
        escape_trap: {
            text: "덫에서 벗어났지만 부상을 입었습니다. 목숨이 하나 줄었습니다.",
            choices: [
                { text: "계속합니다", next: "injured" }
            ]
        },
        call_for_help: {
            text: "도움을 요청했지만 아무도 오지 않았습니다. 목숨이 하나 줄었습니다.",
            choices: [
                { text: "계속합니다", next: "injured" }
            ]
        },
        injured: {
            text: "시작 지점으로 돌아왔습니다. 조심하세요!",
            choices: [
                { text: "성 안으로 들어갑니다", next: "enter_castle" },
                { text: "주변을 탐험합니다", next: "explore_area" }
            ]
        }
    },
    {
        start: {
            text: "어두운 숲에 들어왔습니다.",
            choices: [
                { text: "길을 따라갑니다", next: "follow_path" },
                { text: "주변을 탐색합니다", next: "explore_forest" }
            ]
        },
        follow_path: {
            text: "숲 속에서 은화 주머니를 발견했습니다!",
            choices: [
                { text: "주머니를 열어 봅니다", next: "gain_money" },
                { text: "그냥 지나갑니다", next: "leave_pouch" }
            ]
        },
        explore_forest: {
            text: "길을 잃고 멘탈이 떨어졌습니다.",
            choices: [
                { text: "멘탈을 회복합니다", next: "gain_mental" },
                { text: "포기합니다", next: "lose_mental" }
            ]
        },
        gain_money: {
            text: "돈을 얻었습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        },
        leave_pouch: {
            text: "아무 일도 일어나지 않았습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        },
        gain_mental: {
            text: "멘탈을 회복했습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        },
        lose_mental: {
            text: "멘탈을 잃었습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        }
    },
    {
        start: {
            text: "해적선에서 바다 위를 항해하던 중, 갑작스러운 폭풍우에 휘말려 섬에 불시착했습니다. 구조 기회를 잡을까요?",
            choices: [
                { text: "섬을 탐험합니다", next: "explore_island" },
                { text: "구조를 기다립니다", next: "wait_for_rescue" }
            ]
        },
        explore_island: {
            text: "섬을 탐험하던 중, 유적을 발견했습니다. 더 들여다볼까요?",
            choices: [
                { text: "유적을 조사합니다", next: "explore_ruins" },
                { text: "다른 장소를 탐험합니다", next: "explore_another_place" }
            ]
        },
        wait_for_rescue: {
            text: "구조가 오지 않았습니다. 자원이 고갈되기 전에 다른 해결책을 찾아야 할 것 같습니다.",
            choices: [
                { text: "섬을 탐험합니다", next: "explore_island" },
                { text: "기다립니다", next: "wait_longer" }
            ]
        },
        explore_ruins: {
            text: "유적 속에서 보물을 발견했습니다! 축하합니다!",
            choices: []
        },
        explore_another_place: {
            text: "다른 장소에서는 아무것도 찾지 못했습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        },
        wait_longer: {
            text: "구조가 오지 않았습니다. 자원이 고갈되기 전에 다른 해결책을 찾아야 할 것 같습니다.",
            choices: [
                { text: "섬을 탐험합니다", next: "explore_island" },
                { text: "기다립니다", next: "wait_longer" }
            ]
        }
    },
    {
        start: {
            text: "유적에서 발견한 보물을 통해 마을에서 축제가 열립니다. 참여할까요?",
            choices: [
                { text: "축제에 참여합니다", next: "join_festival" },
                { text: "축제를 지나칩니다", next: "skip_festival" }
            ]
        },
        join_festival: {
            text: "축제에 참여하여 즐거운 시간을 보냈습니다. 마을 사람들의 친밀감이 더해집니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        },
        skip_festival: {
            text: "축제를 지나쳤지만, 보물 발견으로 마을 사람들의 호감도는 상승했습니다.",
            choices: [
                { text: "계속합니다", next: "start" }
            ]
        }
    },
    {
        start: {
            text: "신비로운 동굴을 발견했습니다.",
            choices: [
                { text: "동굴 안으로 들어갑니다", next: "enter_cave" },
                { text: "동굴을 지나칩니다", next: "pass_cave" }
            ]
        },
        enter_cave: {
            text: "동굴 안에서 빛나는 보석을 발견했습니다.",
            choices: [
                { text: "보석을 줍습니다", next: "take_gem" },
                { text: "보석을 무시합니다", next: "ignore_gem" }
            ]
        },
        pass_cave: {
            text: "동굴을 지나쳤습니다. 하지만 멘탈이 떨어졌습니다.",
            choices: [
                { text: "계속 갑니다", next: "continue_path" }
            ]
        },
        take_gem: {
            text: "보석을 주워 돈을 얻었습니다.",
            choices: [
                { text: "계속합니다", next: "continue_path" }
            ]
        },
        ignore_gem: {
            text: "보석을 무시하고 지나갑니다.",
            choices: [
                { text: "계속합니다", next: "continue_path" }
            ]
        },
        continue_path: {
            text: "앞으로 나아갑니다. 조심하세요!",
            choices: [
                { text: "다음 스토리로", next: "start" }
            ]
        }
    },
    // 후속 스토리
    {
        start: {
            text: "보석을 주운 후에, 당신은 길을 따라 계속 갑니다.",
            choices: [
                { text: "북쪽으로 갑니다", next: "north" },
                { text: "남쪽으로 갑니다", next: "south" }
            ]
        },
        north: {
            text: "북쪽으로 가던 중, 다시 동굴을 발견했습니다.",
            choices: [
                { text: "동굴 안으로 들어갑니다", next: "enter_cave" },
                { text: "동굴을 지나칩니다", next: "pass_cave" }
            ]
        },
        south: {
            text: "남쪽으로 가던 중, 야생 동물을 만났습니다.",
            choices: [
                { text: "동물과 싸웁니다", next: "fight_animal" },
                { text: "도망갑니다", next: "run_away" }
            ]
        }
    }
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

    // 게임 시작 후 초기 스토리 표시
    selectNewStory();
    displayStory('start');
    updateStatus();
}

// 새로운 스토리 선택 함수
function selectNewStory() {
    if (usedStories.length === stories.length) {
        usedStories = [];
    }
    let availableStories = stories.filter((_, index) => !usedStories.includes(index));
    let randomIndex = Math.floor(Math.random() * availableStories.length);
    currentStory = availableStories[randomIndex];
    usedStories.push(stories.indexOf(currentStory));
}

// 스토리 표시 함수
function displayStory(storyKey) {
    const scene = currentStory[storyKey];
    storyText.textContent = scene.text;
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
    const storyActions = {
        'take_gem': () => {
            money = Math.min(money + 1, 3);
            selectNewStory();
            displayStory('start');
        },
        'ignore_gem': () => selectNewStory(),
        'continue_path': () => selectNewStory(),
        'pass_cave': () => {
            mental = Math.max(mental - 1, 0);
            selectNewStory();
            displayStory('start');
        },
        'fight_animal': () => {
            lives = Math.max(lives - 1, 0);
            if (lives <= 0) {
                endGame('lose');
            } else {
                selectNewStory();
                displayStory('start');
            }
        },
        'run_away': () => {
            lives = Math.max(lives - 1, 0);
            if (lives <= 0) {
                endGame('lose');
            } else {
                selectNewStory();
                displayStory('start');
            }
        }
    };

    if (next in storyActions) {
        storyActions[next]();
    } else {
        displayStory(next);
    }
    updateStatus();
}

// 게임 종료 함수
function endGame(result) {
    gameOver = true;
    if (result === 'win') {
        storyText.textContent = `축하합니다! 보물을 모두 찾았습니다! 게임에 이겼습니다!`;
    } else {
        storyText.textContent = `모든 목숨을 잃었습니다. 게임 오버!`;
    }
    choicesDiv.innerHTML = '<button onclick="startGame()">게임 다시 시작</button>';
    updateStatus();
}

// 상태 업데이트 함수 (목숨, 멘탈, 돈)
function updateStatus() {
    document.getElementById('lives').textContent = '❤️'.repeat(lives);
    document.getElementById('mental').textContent = '😃'.repeat(mental);
    document.getElementById('money').textContent = '💰'.repeat(money);
    document.getElementById('found_treasures').textContent = '🏆'.repeat(foundTreasures);
}

// 초기화 버튼 클릭 이벤트
resetButton.addEventListener('click', () => {
    // 초기화
    lives = 3;
    mental = 3;
    money = 3;
    gameOver = false;
    foundTreasures = 0;
    usedStories = [];
    // 상태 업데이트
    updateStatus();
    // 게임 시작
    startGame();
});

// 저장된 데이터 불러오기 버튼 클릭 이벤트
loadButton.addEventListener('click', () => {
    // 저장된 데이터 불러오기 로직 구현 필요
    fetch('/load') // 서버에서 저장된 데이터를 불러오는 API 엔드포인트 호출
        .then(response => response.json())
        .then(data => {
            lives = data.lives;
            mental = data.mental;
            money = data.money;
            foundTreasures = data.foundTreasures;
            currentStory = stories[data.currentStoryIndex];
            usedStories = data.usedStories;
            gameOver = false;

            displayStory(data.currentStoryKey);
            updateStatus();
        })
        .catch(error => {
            console.error('Error loading saved data:', error);
        });
});

// 페이지 로드 시 게임 시작
window.onload = startGame;