import sqlite3
import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, \
    QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

DATABASE = 'db/saves.db'
STORY_DATA_FILE = 'assets/story_data.json'

#DB 연결, 테이블 설정
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS game_saves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenes TEXT NOT NULL,
        lives INTEGER NOT NULL,
        sense INTEGER NOT NULL,
        money INTEGER NOT NULL,
        found_treasures INTEGER NOT NULL,
        items TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

#스토리 json 파일 불러오기
def load_story_data():
    with open(STORY_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title_layout = None
        self.title_image_label = None
        self.start_button = None

        self.setWindowTitle("비상식에서 살아남기")
        self.setGeometry(100, 100, 800, 450)  #크기 비율
        self.setMinimumSize(700, 550)   #최소 사이즈

        #초기 리스트, 배열 설정
        self.scenes = []
        self.meet = []
        self.status = {
            "lives": 3,
            "sense": 3,
            "money": 3,
            "found_treasures": 0
        }

        self.setStyleSheet(open("assets/styles/style.qss").read())

        self.layout = QVBoxLayout()

        #게임 시작 시 타이틀 화면 표시
        self.show_title()

        self.setLayout(self.layout)

        #스토리 데이터 불러오기
        self.story_data = load_story_data()
        self.load_scenes()

        self.item_list = QListWidget()
        self.layout.addWidget(self.item_list)
        self.item_list.hide()

    def load_scenes(self):  #배열에 자동(동적) 추가
        self.scenes = [key for key in self.story_data if key.startswith('scenes')]
        self.scenes += [key for key in self.story_data if key.startswith('trader')]

    def show_item_list(self):
        if self.item_list.isVisible():
            self.item_list.hide()
        else:
            self.item_list.show()

    def show_title(self):
        #모든 위젯 제거
        if self.title_layout is not None:
            for i in reversed(range(self.title_layout.count())):
                widget = self.title_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        self.title_layout = QVBoxLayout()

        #제목, 게임 시작 추가
        self.title_image_label = QLabel(self)
        pixmap = QPixmap('assets/images/title/title.png')
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
            "found_treasures": 0
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

        self.final_label = QLabel("스택: 0")

        self.status_layout.addWidget(self.lives_container)
        self.status_layout.addWidget(self.sense_container)
        self.status_layout.addWidget(self.money_container)
        self.status_layout.addWidget(self.final_label)

        self.layout.addLayout(self.status_layout)

        # 스토리 이미지 표시
        self.story_image_label = QLabel(self)
        self.layout.addWidget(self.story_image_label)

        # 스토리 텍스트 표시
        self.story_text_label = QLabel("텍스트 표시", self)
        self.story_text_label.setWordWrap(True)
        self.layout.addWidget(self.story_text_label)

        # 선택지 버튼 레이아웃
        self.choice_buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.choice_buttons_layout)

        self.item_list = QListWidget()  # 여기에서 초기화

        self.show_items_button = QPushButton("아이템 보기")
        self.show_items_button.setFixedSize(100, 50)
        self.show_items_button.clicked.connect(self.show_item_list)
        self.layout.addWidget(self.show_items_button)

        #초기화
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

            self.story_text_label.setText(data['text'])

            if data.get('image'):
                pixmap = QPixmap(data['image']).scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.story_image_label.setPixmap(pixmap)
            else:
                self.story_image_label.clear()

            # 선택지 버튼을 리셋
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

def main():
    init_db()
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
