from flask import render_template, jsonify, request
import random
from app import app  # game.py 파일에서 Flask 인스턴스를 가져옵니다

# 초기 상태 설정
lives = 3
mental = 3
money = 3
gameOver = False
currentStory = None
foundTreasures = 0

usedStories = []
requiredStorySeen = False

# 스토리 데이터
stories = [
    {
        "start": {
            "text": "어두운 숲 1",
            "image": "/static/image/임시 이미지.svg",
            "choices": [
                { "text": "북쪽", "next": "north_path" },
                { "text": "남쪽", "next": "south_path" }
            ]
        },
        "north_path": {
            "text": "보물 발견 1",
            "choices": [
                { "text": "열기", "next": "treasure" },
                { "text": "그냥 두기", "next": "leave_chest" }
            ]
        },
        "south_path": {
            "text": "야생 동물 조우 1",
            "choices": [
                { "text": "싸우기", "next": "fight_animal" },
                { "text": "도망가기", "next": "run_away" }
            ]
        },
        "treasure": {
            "text": "보물 획득",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "leave_chest": {
            "text": "떠나기, 야생동물 조우 2",
            "choices": [
                { "text": "싸우기", "next": "fight_animal" },
                { "text": "도망가기", "next": "run_away" }
            ]
        },
        "fight_animal": {
            "text": "부상, 목숨 감소",
            "choices": [
                { "text": "다음", "next": "next_story" }
            ]
        },
        "run_away": {
            "text": "도망, 목숨 감소",
            "choices": [
                { "text": "다음", "next": "next_story" }
            ]
        },
        "next_story": {
            "text": "다음으로",
            "choices": [
                { "text": "다음", "next": "start"}
            ]
        }
    },
    # 기타 스토리 데이터...
]

@app.route('/start', methods=['POST'])
def start_game():
    global lives, mental, money, gameOver, foundTreasures, usedStories, requiredStorySeen
    lives = 3
    mental = 3
    money = 3
    gameOver = False
    foundTreasures = 0
    usedStories = []
    requiredStorySeen = False

    select_new_story()
    return jsonify({"story": get_current_story("start"), "status": get_status()})

@app.route('/choice', methods=['POST'])
def make_choice():
    global lives, mental, money, gameOver, foundTreasures
    choice = request.json['choice']
    next_story = currentStory[choice]['next']

    if next_story == 'treasure' or next_story == 'inspect_relic':
        foundTreasures += 1
        if foundTreasures >= 2:
            return jsonify({"story": {"text": "축하합니다! 보물을 모두 찾았습니다! 게임에 이겼습니다!"}, "status": get_status()})
        else:
            return jsonify({"story": get_current_story(next_story), "status": get_status()})

    elif next_story in ['fight_animal', 'run_away', 'escape_trap', 'call_for_help']:
        lives -= 1
        if lives <= 0:
            return jsonify({"story": {"text": "모든 목숨을 잃었습니다. 게임 오버!"}, "status": get_status()})
        else:
            return jsonify({"story": get_current_story(next_story), "status": get_status()})

    elif next_story in ['explore_forest', 'pass_cave', 'lose_mental']:
        mental -= 1
        if mental <= 0:
            return jsonify({"story": {"text": "모든 멘탈을 잃었습니다. 게임 오버!"}, "status": get_status()})
        else:
            return jsonify({"story": get_current_story(next_story), "status": get_status()})

    elif next_story == 'gain_money':
        money += 1
        return jsonify({"story": get_current_story(next_story), "status": get_status()})

    elif next_story == 'gain_mental':
        mental += 1
        return jsonify({"story": get_current_story(next_story), "status": get_status()})

    elif next_story == 'next_story':
        select_new_story()
        return jsonify({"story": get_current_story("start"), "status": get_status()})

    else:
        return jsonify({"story": get_current_story(next_story), "status": get_status()})

def select_new_story():
    global currentStory, usedStories, requiredStorySeen
    available_stories = [story for i, story in enumerate(stories) if i not in usedStories]
    
    if not requiredStorySeen:
        available_stories = [story for story in available_stories if not story.get('isFollowUp')]

    currentStory = random.choice(available_stories)
    usedStories.append(stories.index(currentStory))
    
    if currentStory.get('requiresPrevious'):
        requiredStorySeen = True

def get_current_story(story_key):
    scene = currentStory[story_key]
    return {"text": scene['text'], "choices": scene['choices']}

def get_status():
    return {
        "lives": lives,
        "mental": mental,
        "money": money,
        "foundTreasures": foundTreasures
    }

if __name__ == '__main__':
    app.run(debug=True)
