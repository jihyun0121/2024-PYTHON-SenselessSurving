function updateStatus(status) {
    const heartFull = '<img src="/static/image/체력.svg" />';
    const heartEmpty = '<img src="/static/image/체력 감소.svg" />';
    const brainFull = '<img src="/static/image/지능.svg" />';
    const brainEmpty = '<img src="/static/image/지능 감소.svg" />';
    const moneyFull = '<img src="/static/image/돈.svg" />';
    const moneyEmpty = '<img src="/static/image/돈 감소.svg" />';
    const treasureIcon = '✨';

    document.getElementById('lives').innerHTML = heartFull.repeat(status.lives) + heartEmpty.repeat(3 - status.lives);
    document.getElementById('mental').innerHTML = brainFull.repeat(status.mental) + brainEmpty.repeat(3 - status.mental);
    document.getElementById('money').innerHTML = moneyFull.repeat(status.money) + moneyEmpty.repeat(3 - status.money);
    document.getElementById('found_treasures').innerHTML = treasureIcon.repeat(status.found_treasures);
}

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

function updateItems(items) {
    const itemsElement = document.getElementById('items');
    itemsElement.innerHTML = '';
    items.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = item;
        itemsElement.appendChild(listItem);
    });
}

function displayScene(data) {
    const storyTextElement = document.getElementById('story-text');
    storyTextElement.textContent = data.text;
    if (data.image) {
        const imgElement = document.createElement('img');
        imgElement.src = data.image;
        imgElement.alt = "Story Image";
        storyTextElement.insertBefore(imgElement, storyTextElement.firstChild);
    }

    const choicesElement = document.getElementById('choices');
    choicesElement.innerHTML = '';
    data.choices.forEach((choice) => {
        const button = document.createElement('button');
        button.textContent = choice.text;
        button.classList.add('choice');
        button.dataset.next = choice.next;
        choicesElement.appendChild(button);
    });

    updateStatus(data.status);
    updateItems(data.items);
}

function startGame() {
    fetch('/start_game', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => displayScene(data))
    .catch(error => {
        console.error('Error:', error);
        alert('게임을 시작하는 중 오류가 발생했습니다. 페이지를 새로고침 해주세요.');
    });
}

function makeChoice(next) {
    fetch('/make_choice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({choice: next}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        if (data.game_over) {
            alert(data.message);
            startGame();
        } else {
            displayScene(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('선택을 처리하는 중 오류가 발생했습니다. 게임을 다시 시작합니다.');
        startGame();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    startGame();

    document.getElementById('choices').addEventListener('click', function(event) {
        if (event.target.classList.contains('choice')) {
            const next = event.target.dataset.next;
            makeChoice(next);
        }
    });

    document.getElementById('reset-button').addEventListener('click', startGame);
});