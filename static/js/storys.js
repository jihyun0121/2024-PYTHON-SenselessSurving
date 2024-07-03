export const stories = [
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
    }
];
