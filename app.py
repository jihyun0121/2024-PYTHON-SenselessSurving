import sqlite3
import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, \
    QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

DATABASE = 'db/saves.db'
STORY_DATA_FILE = 'assets/story_data.json'


# DB 연결 및 테이블 설정
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


# 스토리 json 파일 불러오기
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
        self.setMinimumSize(700, 550)

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

        # 게임 시작 시 타이틀 화면 표시
        self.show_title()

        self.setLayout(self.layout)

        # 스토리 데이터를 불러옴
        self.story_data = load_story_data()
        self.load_scenes()

        self.item_list = QListWidget()  # 여기에서 초기화
        self.layout.addWidget(self.item_list)
        self.item_list.hide()  # 초기에는 아이템 목록을 숨깁니다.

    def load_scenes(self):
        # scenes 카테고리를 동적으로 로드
        self.scenes = [key for key in self.story_data if key.startswith('scenes')]
        self.scenes += [key for key in self.story_data if key.startswith('trader')]

    def show_item_list(self):
        # 아이템 목록을 보이거나 숨김
        if self.item_list.isVisible():
            self.item_list.hide()
        else:
            self.item_list.show()

    def show_title(self):
        # 모든 위젯을 제거
        if self.title_layout is not None:  # None 체크 추가
            for i in reversed(range(self.title_layout.count())):
                widget = self.title_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

        self.title_layout = QVBoxLayout()

        # 제목, 게임 시작 추가
        self.title_image_label = QLabel(self)
        pixmap = QPixmap('assets/images/title/title.png')
        self.title_image_label.setPixmap(pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.title_layout.addWidget(self.title_image_label)

        self.start_button = QPushButton(" ")  # 텍스트를 공백으로 설정
        self.start_button.setStyleSheet("background-image: url('assets/images/title/start_btn.png');"
                                        "background-repeat: no-repeat;"
                                        "background-position: center;")
        self.start_button.clicked.connect(self.start_game)
        self.title_layout.addWidget(self.start_button)

        self.layout.addLayout(self.title_layout)

    def start_game(self):
        QMessageBox.information(self, "게임 시작", "게임이 시작되었습니다!")


def main():
    init_db()
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
