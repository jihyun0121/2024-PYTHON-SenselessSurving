import { stories } from './storys.js';
import { makeChoice } from './choices.js';

const storyText = document.getElementById('story-text');
const choicesDiv = document.getElementById('choices');
const statusDiv = document.getElementById('status');

// 초기 상태 설정
let state = {
    lives: 3,
    mental: 3,
    money: 3,
    gameOver: false,
    currentStory: null,
    foundTreasures: 0,
    totalTreasures: 2, // 보물의 총 개수
    usedStories: []
};

// 게임 시작 함수
function startGame() {
    // 초기화
    state = {
        lives: 3,
        mental: 3,
        money: 3,
        gameOver: false,
        currentStory: null,
        foundTreasures: 0,
        totalTreasures: 2, // 보물의 총 개수
        usedStories: []
    };

    // 게임 시작 후 초기 스토리 표시
    selectNewStory();
    updateStatus();
    displayStory('start');
}

// 새로운 스토리 선택 함수
function selectNewStory() {
    if (state.usedStories.length === stories.length) {
        state.usedStories = [];
    }
    let availableStories = stories.filter((_, index) => !state.usedStories.includes(index));
    let randomIndex = Math.floor(Math.random() * availableStories.length);
    state.currentStory = availableStories[randomIndex];
    state.usedStories.push(stories.indexOf(state.currentStory));
}

// 스토리 표시 함수
function displayStory(storyKey) {
    const scene = state.currentStory[storyKey];
    storyText.textContent = scene.text;
    choicesDiv.innerHTML = '';

    scene.choices.forEach(choice => {
        const button = document.createElement('button');
        button.textContent = choice.text;
        button.addEventListener('click', () => makeChoice(choice.next, state, selectNewStory, displayStory, endGame, updateStatus));
        choicesDiv.appendChild(button);
    });
}

// 게임 종료 함수
function endGame(result) {
    state.gameOver = true;
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
    document.getElementById('lives').textContent = '❤️'.repeat(state.lives);
    document.getElementById('mental').textContent = '😃'.repeat(state.mental);
    document.getElementById('money').textContent = '💰'.repeat(state.money);
    document.getElementById('found_treasures').textContent = '🏆'.repeat(state.foundTreasures);
}

// 페이지 로드 시 게임 시작
window.onload = startGame;
