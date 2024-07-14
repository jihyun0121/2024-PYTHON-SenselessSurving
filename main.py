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
    {   # 어두운 숲 1 스토리
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
    {   # 오래된 성 스토리
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
    {   # 신비한 동굴
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
    {   # 신비한 동굴 후속 스토리
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
    {   # 어두운 숲 2 스토리
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
    }#,
    # {   #섬 스토리
    #     start: {
    #         text: "섬에 갇힘",
    #         image: "/static/image/임시 이미지.svg",
    #         choices: [
    #             { text: "탐험하기", next: "explore_island" },
    #             { text: "구조 기다리기", next: "wait_for_rescue" }
    #         ]
    #     },
    #     explore_island: {
    #         text: "유적 발견",
    #         choices: [
    #             { text: "유적 조사", next: "explore_ruins" },
    #             { text: "다른 곳 탐험하기", next: "explore_another_place" }
    #         ]
    #     },
    #     wait_for_rescue: {
    #         text: "구조 반응 없음",
    #         choices: [
    #             { text: "섬 탐험하기", next: "explore_island" },
    #             { text: "기다리기", next: "wait_longer" }
    #         ]
    #     },
    #     explore_ruins: {
    #         text: "보물 발견",
    #         choices: [
    #             { text: "계속합니다", next: "next_story" }
    #         ]
    #     },
    #     explore_another_place: {
    #         text: "아무것도 없음",
    #         choices: [
    #             { text: "계속합니다", next: "explore_island" }
    #         ]
    #     },
    #     wait_longer: {
    #         text: "여전히 구조 반응 없음",
    #         choices: [
    #             { text: "섬을 탐험합니다", next: "explore_island" },
    #             { text: "기다립니다", next: "wait_longer" }
    #         ]
    #     },
    #     next_story: {
    #         text: "다음으로",
    #         choices: [
    #             { text: "다음", next: "start"}
    #         ]
    #     },
    #     isFollowUp: false,
    #     key: "island_story"
    # },
    # {   # 섬 후속 스토리
    #     start: {
    #         text: "마을 축제",
    #         image: "/static/image/임시 이미지.svg",
    #         choices: [
    #             { text: "참여하기", next: "join_festival" },
    #             { text: "무시하기", next: "ignore_festival" }
    #         ]
    #     },
    #     join_festival: {
    #         text: "정보와 새로운 친구",
    #         choices: [
    #             { text: "계속", next: "next_story" }
    #         ]
    #     },
    #     ignore_festival: {
    #         text: "무시하고 탐험 계속",
    #         choices: [
    #             { text: "계속", next: "next_story" }
    #         ]
    #     },
    #     next_story: {
    #         text: "다음으로",
    #         choices: [
    #             { text: "다음", next: "start"}
    #         ]
    #     },
    #     isFollowUp: true,
    #     key: "follow_up_story"
    # }
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
