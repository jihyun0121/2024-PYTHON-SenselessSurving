from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 게임 상태 초기화
game_state = {
    "lives": 3,
    "mental": 3,
    "money": 3,
    "found_treasures": 0,
    "used_stories": [],
    "required_story_seen": False,
    "current_story": None
}

# Story data
stories = [
    {   # 어두운 숲 1 스토리
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
    {   # 오래된 성 스토리
        "start": {
            "text": "오래된 성",
            "image": "/static/image/임시 이미지.svg",
            "choices": [
                { "text": "들어가기", "next": "enter_castle" },
                { "text": "주변 탐험", "next": "explore_area" }
            ]
        },
        "enter_castle": {
            "text": "고대 유물 발견 1",
            "choices": [
                { "text": "유물 조사", "next": "inspect_relic" },
                { "text": "유물 무시", "next": "ignore_relic" }
            ]
        },
        "explore_area": {
            "text": "탐험, 덫 걸림",
            "choices": [
                { "text": "벗어나기", "next": "escape_trap" },
                { "text": "도움 요청", "next": "call_for_help" }
            ]
        },
        "inspect_relic": {
            "text": "유물 조사, 보물발견 2",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "ignore_relic": {
            "text": "유물 무시, 덫 걸림.",
            "choices": [
                { "text": "덫에서 벗어납니다", "next": "escape_trap" },
                { "text": "도움을 요청합니다", "next": "call_for_help" }
            ]
        },
        "escape_trap": {
            "text": "부상, 목숨 감소",
            "choices": [
                { "text": "다음", "next": "next_story" }
            ]
        },
        "call_for_help": {
            "text": "도움 요청, 목숨 감소",
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
    {   # 신비한 동굴
        "start": {
            "text": "신비로운 동굴 발견",
            "image": "/static/image/임시 이미지.svg",
            "choices": [
                { "text": "들어가기", "next": "enter_cave" },
                { "text": "지나기기", "next": "pass_cave" }
            ]
        },
        "enter_cave": {
            "text": "보석 발견",
            "choices": [
                { "text": "줍기", "next": "take_gem" },
                { "text": "무시하기", "next": "ignore_gem" }
            ]
        },
        "pass_cave": {
            "text": "지나침, 멘탈 감소",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "take_gem": {
            "text": "보석 획득, 돈 회복",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ],
            "item": "보석"  # 획득 아이템 추가
        },
        "ignore_gem": {
            "text": "보석 무시",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "next_story": {
            "text": "다음으로",
            "choices": [
                { "text": "다음", "next": "start"}
            ]
        },
        "isFollowUp": False
    },
    {   # 신비한 동굴 후속 스토리
        "start": {
            "text": "갈림길",
            "image": "/static/image/임시 이미지.svg",
            "choices": [
                { "text": "북쪽", "next": "north_path" },
                { "text": "남쪽", "next": "south_path" }
            ]
        },
        "north_path": {
            "text": "북쪽, 동굴 발견",
            "choices": [
                { "text": "들어가기", "next": "enter_cave" },
                { "text": "지나치기", "next": "pass_cave" }
            ]
        },
        "south_path": {
            "text": "남쪽, 야생 동물 조우",
            "choices": [
                { "text": "싸우기", "next": "fight_animal" },
                { "text": "도망", "next": "run_away" }
            ]
        },
        "enter_cave": {
            "text": "고대 유물 발견 2",
            "choices": [
                { "text": "유물 조사", "next": "inspect_relic" },
                { "text": "유물 무시", "next": "ignore_relic" }
            ]
        },
        "inspect_relic": {
            "text": "유물 조사, 보물발견 3",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "ignore_relic": {
            "text": "유물 무시, 덫 걸림.",
            "choices": [
                { "text": "덫에서 벗어납니다", "next": "escape_trap" },
                { "text": "도움을 요청합니다", "next": "call_for_help" }
            ]
        },
        "escape_trap": {
            "text": "부상, 목숨 감소",
            "choices": [
                { "text": "다음", "next": "next_story" }
            ]
        },
        "call_for_help": {
            "text": "도움 요청, 목숨 감소",
            "choices": [
                { "text": "다음", "next": "next_story" }
            ]
        },
        "next_story": {
            "text": "다음으로",
            "choices": [
                { "text": "다음", "next": "start"}
            ]
        },
        "requiresPrevious": True,
        "isFollowUp": True
    },
    {   # 어두운 숲 2 스토리
        "start": {
            "text": "어두운 숲2",
            "image": "/static/image/임시 이미지.svg",
            "choices": [
                { "text": "나아가기", "next": "follow_path" },
                { "text": "탐색하기", "next": "explore_forest" }
            ]
        },
        "follow_path": {
            "text": "은화 주머니 발견",
            "choices": [
                { "text": "열어보기", "next": "gain_money" },
                { "text": "지나가기", "next": "leave_pouch" }
            ]
        },
        "explore_forest": {
            "text": "길 잃기, 멘탈 감소",
            "choices": [
                { "text": "정신 차리기", "next": "gain_mental" },
                { "text": "포기", "next": "lose_mental" }
            ]
        },
        "gain_money": {
            "text": "돈 회복",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "leave_pouch": {
            "text": "아무것도 없음",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "gain_mental": {
            "text": "멘탈 회복",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "lose_mental": {
            "text": "멘탈 감소",
            "choices": [
                { "text": "계속", "next": "next_story" }
            ]
        },
        "next_story": {
            "text": "다음으로",
            "choices": [
                { "text": "다음", "next": "start"}
            ]
        }
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def about():
    return render_template('main.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game_state
    game_state = {
        "lives": 3,
        "mental": 3,
        "money": 3,
        "found_treasures": 0,
        "used_stories": [],
        "required_story_seen": False,
        "current_story": None,
        "items": []  # 게임 상태 초기화 시 아이템 리스트도 초기화
    }
    select_new_story()
    return get_current_scene('start')

@app.route('/make_choice', methods=['POST'])
def make_choice():
    data = request.get_json()
    if not data or 'choice' not in data:
        return jsonify({"error": "Invalid request"}), 400
    choice = data['choice']
    return get_current_scene(choice)

def select_new_story():
    global game_state
    if len(game_state["used_stories"]) == len(stories):
        return None

    available_stories = [story for i, story in enumerate(stories) if i not in game_state["used_stories"]]
    
    if not game_state["required_story_seen"]:
        available_stories = [story for story in available_stories if not story.get('isFollowUp', False)]
    
    game_state["current_story"] = random.choice(available_stories)
    game_state["used_stories"].append(stories.index(game_state["current_story"]))
    
    if game_state["current_story"].get('requiresPrevious', False):
        game_state["required_story_seen"] = True

def get_current_scene(scene_key):
    global game_state
    if not game_state["current_story"] or scene_key not in game_state["current_story"]:
        return jsonify({"error": "Invalid scene"}), 400

    scene = game_state["current_story"][scene_key]
    
    # 아이템 획득 처리
    if "item" in scene:
        game_state["items"].append(scene["item"])

    if scene_key in ['treasure', 'inspect_relic', 'explore_ruins']:
        game_state["found_treasures"] += 1
        if game_state["found_treasures"] >= 2:
            return end_game('win')
    elif scene_key in ['fight_animal', 'run_away', 'escape_trap', 'call_for_help']:
        game_state["lives"] -= 1
        if game_state["lives"] <= 0:
            return end_game('lose')
    elif scene_key in ['explore_forest', 'pass_cave', 'lose_mental']:
        game_state["mental"] -= 1
        if game_state["mental"] <= 0:
            return end_game('lose')
    elif scene_key == 'gain_money':
        if game_state["money"] < 3:
            game_state["money"] += 1
    elif scene_key == 'gain_mental':
        if game_state["mental"] < 3:
            game_state["mental"] += 1
    elif scene_key == 'next_story':
        select_new_story()
        return get_current_scene('start')

    return jsonify({
        "text": scene["text"],
        "image": scene.get("image"),
        "choices": scene["choices"],
        "status": {
            "lives": game_state["lives"],
            "mental": game_state["mental"],
            "money": game_state["money"],
            "found_treasures": game_state["found_treasures"],
            "items": game_state["items"]
        }
    })

def end_game(result):
    message = ""
    if result == 'win':
        message = "축하합니다! 보물을 모두 찾았습니다! 게임에 이겼습니다!"
    elif len(game_state["used_stories"]) == len(stories):
        message = "탐험을 완료하였습니다"
    elif game_state["lives"] == 0:
        message = "모든 목숨을 잃었습니다. 게임 오버!"
    elif game_state["mental"] == 0:
        message = "모든 멘탈을 잃었습니다. 게임 오버!"
    
    return jsonify({
        "game_over": True,
        "message": message,
        "status": game_state
    })

if __name__ == "__main__":
    app.run(debug=True)