async function saveChoice(event) {
    event.preventDefault();
    const formData = new FormData(document.getElementById('gameForm'));
    try {
        const response = await fetch('/save_choice', {
            method: 'POST',
            body: formData
        });
        const story = await response.json();
        updateGame(story);
    } catch (error) {
        console.error('Error saving choice:', error);
    }
}

function updateGame(story) {
    const storyTextElement = document.getElementById('story-text');
    storyTextElement.textContent = story.start.text;

    const choicesElement = document.getElementById('choices');
    choicesElement.innerHTML = '';
    story.start.choices.forEach(choice => {
        const button = document.createElement('button');
        button.textContent = choice.text;
        button.addEventListener('click', () => {
            document.getElementById('story_key').value = choice.next;
            document.getElementById('story_text').value = story.start.text;
            document.getElementById('next_choices').value = JSON.stringify(story[choice.next].choices);
            document.getElementById('found_at').value = story.isFollowUp === 'true' && choice.next === 'treasure' ? 'treasure' : '';
            document.getElementById('gameForm').submit();
        });
        choicesElement.appendChild(button);
    });

    const statusElements = {
        'lives': document.getElementById('lives'),
        'mental': document.getElementById('mental'),
        'money': document.getElementById('money'),
        'found_treasures': document.getElementById('found_treasures')
    };
    Object.keys(statusElements).forEach(key => {
        statusElements[key].textContent = story[key] || '';
    });
}

async function resetGame() {
    try {
        const response = await fetch('/', {
            method: 'GET'
        });
        const story = await response.json();
        updateGame(story);
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

document.getElementById('reset-button').addEventListener('click', resetGame);

document.addEventListener('DOMContentLoaded', resetGame);