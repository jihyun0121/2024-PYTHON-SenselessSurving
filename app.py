import json
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, \
    QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

STORY_DATA_FILE = 'assets/story_data.json'


def load_story_data():
    with open(STORY_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.item_label = None
        self.title_layout = None
        self.title_image_label = None
        self.start_button = None

        self.lives_container = None
        self.status_layout = None
        self.lives_layout = None
        self.lives_label = None

        self.sense_container = None
        self.sense_layout = None
        self.sense_label = None

        self.money_container = None
        self.money_layout = None
        self.money_label = None

        self.final_label = None

        self.story_image_label = None
        self.story_text_label = None
        self.choice_buttons_layout = None
        self.show_items_button = None

        self.current_category = None
        self.show_items_button = None
        self.reset_button = None

        self.setWindowTitle("비상식에서 살아남기")
        self.setGeometry(100, 100, 800, 450)
        self.setMinimumSize(700, 550)

        # 초기 리스트, 배열 설정
        self.scenes = []
        self.Q_correct = 0
        self.status = {
            "lives": 3,
            "sense": 3,
            "money": 3,
            "end_correct": 0
        }

        self.setStyleSheet(open("assets/styles/style.qss").read())

        self.layout = QVBoxLayout()

        # 게임 시작 시 타이틀 화면 표시
        self.show_title()

        self.setLayout(self.layout)

        # 스토리 데이터를 불러옴
        self.story_data = load_story_data()
        self.load_scenes()

        self.item_list = QListWidget()  # 아이템 목록
        self.layout.addWidget(self.item_list)
        self.item_list.hide()

        self.current_text = ""
        self.text_index = 0
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.update_typing_effect)

    def load_scenes(self):
        # scenes 자동(동적) 추가
        self.scenes = [key for key in self.story_data if key.startswith('scenes')]
        self.scenes += [key for key in self.story_data if key.startswith('trader')]
        self.scenes += [key for key in self.story_data if key.startswith('meet')]

    def show_item_list(self):
        # 아이템 목록을 보이거나 숨김
        if self.item_list.isVisible():
            self.item_list.hide()
        else:
            self.item_list.show()

    def show_title(self):
        # 모든 위젯 제거
        if self.title_layout is not None:
            for i in reversed(range(self.title_layout.count())):
                widget = self.title_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        self.title_layout = QVBoxLayout()

        # 제목, 게임 시작 추가
        self.title_image_label = QLabel(self)
        pixmap = QPixmap('assets/images/title.png')
        self.title_image_label.setPixmap(pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.title_layout.addWidget(self.title_image_label)

        self.start_button = QPushButton("게임 시작")
        self.start_button.clicked.connect(self.start_game)
        self.title_layout.addWidget(self.start_button)

        self.layout.addLayout(self.title_layout)

    def start_game(self):
        self.status = {
            "lives": 3,
            "sense": 3,
            "money": 3,
            "end_correct": 0
        }

        self.title_image_label.hide()  # 타이틀, 시작 버튼 숨기기
        self.start_button.hide()

        self.load_scenes()

        self.status_layout = QHBoxLayout()

        self.lives_container = QWidget()
        self.lives_layout = QVBoxLayout()
        self.lives_container.setLayout(self.lives_layout)
        self.lives_label = QLabel()
        self.lives_layout.addWidget(self.lives_label)

        self.sense_container = QWidget()
        self.sense_layout = QVBoxLayout()
        self.sense_container.setLayout(self.sense_layout)
        self.sense_label = QLabel()
        self.sense_layout.addWidget(self.sense_label)

        self.money_container = QWidget()
        self.money_layout = QVBoxLayout()
        self.money_container.setLayout(self.money_layout)
        self.money_label = QLabel()
        self.money_layout.addWidget(self.money_label)

        self.final_label = QLabel("엔딩: 0")

        self.status_layout.addWidget(self.lives_container)
        self.status_layout.addWidget(self.sense_container)
        self.status_layout.addWidget(self.money_container)
        self.status_layout.addWidget(self.final_label)

        self.layout.addLayout(self.status_layout)

        # 스토리 이미지
        self.story_image_label = QLabel(self)
        self.layout.addWidget(self.story_image_label)

        # 스토리 텍스트
        self.story_text_label = QLabel("텍스트 표시", self)
        self.story_text_label.setWordWrap(True)
        self.layout.addWidget(self.story_text_label)

        # 선택지 버튼
        self.choice_buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.choice_buttons_layout)

        self.item_list = QListWidget()

        self.show_items_button = QPushButton("아이템 보기")
        self.show_items_button.setFixedSize(100, 50)
        self.show_items_button.clicked.connect(self.show_item_list)
        self.layout.addWidget(self.show_items_button)

        # 초기화
        self.reset_button = QPushButton("초기화")
        self.reset_button.setFixedSize(100, 50)
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        # 게임 시작 데이터 로드
        self.display_scene('intro', 'start_game')

    def display_scene(self, category, scene_name):
        self.current_category = category

        try:
            data = self.story_data[category][scene_name]

            self.start_typing_effect(data['text'])  # 타이핑 효과 적용

            if data.get('image'):
                pixmap = QPixmap(data['image']).scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.story_image_label.setPixmap(pixmap)
            else:
                self.story_image_label.clear()

            # 선택지 버튼 리셋
            self.reset_choice()

            # 새로운 선택지 버튼 추가
            for choice in data['choices']:
                button = QPushButton(choice['text'])
                button.clicked.connect(
                    lambda checked, next=choice['next'], action_id=choice['id']: self.make_choice(next, action_id))
                self.choice_buttons_layout.addWidget(button)

            # 상태 및 아이템 업데이트 (초기 설정)
            self.update_status(data.get('status', {}))
            self.get_items(data.get('items', []))

        except KeyError as e:
            QMessageBox.critical(self, "에러", f"장면 '{scene_name}' 또는 카테고리 '{category}'을(를) 찾을 수 없습니다. 오류: {e}")

    def update_status(self, status):
        lives = status.get('lives', self.status['lives'])
        sense = status.get('sense', self.status['sense'])
        money = status.get('money', self.status['money'])
        end_correct = status.get('end_correct', self.status['end_correct'])

        self.lives_label.setText(f"목숨: {'❤️' * lives}")
        self.sense_label.setText(f"멘탈: {'📝' * sense}")
        self.money_label.setText(f"돈: {'💰' * money}")
        self.final_label.setText(f"상식: {'✨' * end_correct}")

        if self.status['lives'] <= 0 or self.status['sense'] <= 0:
            if self.current_category != "ending":  # ending 호출한 경우 방지 (무한 재귀호출 에러 발생..)
                self.display_scene("ending", "ending0")
            return

    def reset_choice(self):
        for i in reversed(range(self.choice_buttons_layout.count())):
            widget = self.choice_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def reset_game(self):
        # 현재 레이아웃의 모든 위젯과 레이아웃을 제거
        def clear_layout(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    elif item.layout():
                        clear_layout(item.layout())

        clear_layout(self.layout)

        # 게임에서 사용된 추가 레이아웃 초기화
        if hasattr(self, 'status_layout'):
            clear_layout(self.status_layout)
            self.status_layout.deleteLater()
            del self.status_layout

        if hasattr(self, 'choice_buttons_layout'):
            clear_layout(self.choice_buttons_layout)
            self.choice_buttons_layout.deleteLater()
            del self.choice_buttons_layout

        # 아이템 목록 삭제
        if hasattr(self, 'item_list'):
            self.item_list.deleteLater()
            del self.item_list

        # 게임 상태 초기화
        self.status = {
            "lives": 3,
            "sense": 3,
            "money": 3,
            "end_correct": 0
        }

        # 남은 scenes 리스트 초기화
        self.load_scenes()

        # 타이틀 화면을 다시 표시
        self.show_title()

    def get_items(self, items):
        item_dict = {}

        print(f"현재 추가된 아이템: {items}")  # 배열 확인용

        # 아이템 개수 세기
        for item in items:
            if item in item_dict:
                item_dict[item] += 1
            else:
                item_dict[item] = 1

        # 리스트에 있는 아이템 업데이트
        for i in range(self.item_list.count()):
            item_text = self.item_list.item(i).text()
            item_name = item_text.split(" x ")[0]
            if item_name in item_dict:
                new_count = item_dict[item_name] + int(item_text.split(" x ")[1])  # 기존 개수에 더함
                self.item_list.item(i).setText(f"{item_name} x {new_count}")
                del item_dict[item_name]  # 이미 처리한 아이템은 삭제

        # 새로운 아이템 추가
        for item, count in item_dict.items():
            if count > 0:  # 개수가 0보다 클 때만 추가
                list_item = QListWidgetItem(f"{item} x {count}")
                self.item_list.addItem(list_item)

    def lose_items(self, items):
        matching_items = [self.item_list.item(i) for i in range(self.item_list.count()) if
                          items in self.item_list.item(i).text()]

        if matching_items:
            current_item = matching_items[0]
            current_text = current_item.text()
            current_count = int(current_text.split(" x ")[1])
            new_count = current_count - 1

            if new_count > 0:
                current_item.setText(f"{items} x {new_count}")
            else:
                self.item_list.takeItem(self.item_list.row(current_item))
            return True
        else:
            self.show_message(f"{items} 부족")
            return False

    def get_Ability(self, ability):
        item_dict = {}

        for item in ability:
            if item in item_dict:
                item_dict[item] += 1
            else:
                item_dict[item] = 1

        for i in range(self.item_list.count()):
            item_text = self.item_list.item(i).text()
            item_name = item_text.split(" lv. ")[0]
            if item_name in item_dict:
                new_count = item_dict[ability] + int(item_text.split(" x ")[1])
                self.item_list.item(i).setText(f"{ability} x {new_count}")
                del item_dict[ability]

        for item, count in item_dict.items():
            if count > 0:
                list_item = QListWidgetItem(f"{item} lv. {count}")
                self.item_list.addItem(list_item)

    def lose_Ability(self, ability):
        matching_items = [self.item_list.item(i) for i in range(self.item_list.count()) if
                          ability in self.item_list.item(i).text()]

        if matching_items:
            current_item = matching_items[0]
            current_text = current_item.text()

            current_count = int(current_text.split(" lv. ")[1])

            new_count = current_count - 1

            if new_count > 0:
                current_item.setText(f"{ability} lv. {new_count}")
            else:
                self.item_list.takeItem(self.item_list.row(current_item))
        else:
            self.show_message(f"{ability} 부족")
            return False

    def make_choice(self, next_scene, action_id):
        current_category = self.current_category
        Q_correct = 0

        action_id = [id.strip() for id in action_id.split(",")]

        for id in action_id:
            if id == "none":
                continue
            elif id == "get_live" and self.status['lives'] < 3:
                self.status['lives'] += 1
            elif id == "lose_live":
                self.status['lives'] -= 1

            elif id == "get_sense" and self.status['sense'] < 3:
                self.status['sense'] += 1
            elif id == "lose_sense":
                self.status['sense'] -= 1

            elif id == "get_money" and self.status['money'] < 3:
                self.status['money'] += 1
            elif id == "lose_money":
                if self.status['money'] == 0:
                    self.show_message("돈이 부족합니다!")
                    return
                else:
                    self.status['money'] -= 1

            elif id == "get_map":
                self.get_items(["지도"])
            elif id == "lose_map":
                if not self.lose_items("지도"):  # lose_items에서 false return하면 화면전환 x
                    return

            elif id == "get_gem":
                self.get_items(["보석"])
            elif id == "lose_gem":
                if not self.lose_items("보석"):
                    return

            elif id == "get_shoes":
                self.get_items(["운동화"])
            elif id == "lose_shoes":
                if not self.lose_items("운동화"):
                    return

            elif id == "get_umbrella":
                self.get_items(["우산"])
            elif id == "lose_umbrella":
                if not self.lose_items("우산"):
                    return

            elif id == "get_padding":
                self.get_items(["롱패딩"])
            elif id == "lose_padding":
                if not self.lose_items("롱패딩"):
                    return

            elif id == "get_book":
                self.get_items(["책"])
            elif id == "lose_book":
                if not self.lose_items("책"):
                    return

            elif id == "get_cake":
                self.get_items(["케이크"])
            elif id == "lose_cake":
                if not self.lose_items("케이크"):
                    return

            elif id == "get_healthy":
                self.get_Ability(["근력"])
            elif id == "lose_healthy":
                if not self.lose_Ability("근력"):
                    return

            elif id == "get_intuition":
                self.get_Ability(["강력한 직감"])
            elif id == "lose_intuition":
                if not self.lose_Ability("강력한 직감"):
                    return

            elif id == "get_handmade":
                self.get_Ability(["손재주"])
            elif id == "lose_handmade":
                if not self.lose_Ability("손재주"):
                    return

            elif id == "get_musician":
                self.get_Ability(["음악적 재능"])
            elif id == "lose_musician":
                if not self.lose_Ability("음악적 재능"):
                    return

            elif id == "get_emergency":
                self.get_Ability(["응급치료술"])
            elif id == "lose_emergency":
                if not self.lose_Ability("응급치료술"):
                    return

            elif id == "get_agile":
                self.get_Ability(["날렵함"])
            elif id == "lose_agile":
                if not self.lose_Ability("날렵함"):
                    return

            elif id == "get_lock":
                self.get_Ability(["자물쇠 따기"])
            elif id == "lose_lock":
                if not self.lose_Ability("자물쇠 따기"):
                    return

            elif id == "quiz":
                self.Q_correct = 0
            elif id == "correct":
                self.Q_correct += 1
                if self.Q_correct == 3:
                    self.status['end_correct'] += 1
                    self.Q_correct = 0

        # 상태 업데이트
        self.update_status(self.status)

        # 다음 장면으로 이동
        if "/" in next_scene:
            category, scene_name = next_scene.split("/")
            self.display_scene(category, scene_name)
        elif next_scene == "random_story":
            if len(self.scenes) > 0:  # 남은 랜덤 장면이 있는 경우
                random_scene = random.choice(self.scenes) + '/first'
                category, scene_name = random_scene.split('/')
                self.display_scene(category, scene_name)
                self.scenes.remove(category)
            else:
                self.display_scene("ending", "ending0-0")
        elif next_scene == "start_game":
            self.reset_game()
            self.show_title()
        elif next_scene == "end_game" or len(self.scenes) == 0:
            if self.status['end_correct'] >= 3:
                self.display_scene("ending", "ending3")
            elif 0 < self.status['end_correct'] < 3:
                self.display_scene("ending", "ending2")
            else:
                self.display_scene("ending", "ending1")
        elif next_scene == "quit":
            QApplication.quit()
        else:
            self.display_scene(current_category, next_scene)

    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("경고")
        msg.exec()

    def start_typing_effect(self, text):
        self.current_text = text
        self.text_index = 0
        self.story_text_label.setText("")
        self.typing_timer.start(20)  # 타이머 설정 (50초 마다 글자 추가)

    def update_typing_effect(self):
        if not hasattr(self, 'story_text_label') or self.story_text_label is None:
            return

        try:
            self.story_text_label.setText(self.story_text_label.text() + self.current_text[self.text_index])
            self.text_index += 1

            if self.text_index >= len(self.current_text):
                self.typing_timer.stop()
        except RuntimeError as e:
            print("Error updating typing effect:", e)
            self.typing_timer.stop()


def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
