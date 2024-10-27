import sqlite3
import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, \
    QListWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

DATABASE = 'db/saves.db'
STORY_DATA_FILE = 'assets/story_data.json'


#DB 연결 및 테이블 설정
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

        self.setWindowTitle("비상식에서 살아남기")
        self.setGeometry(100, 100, 800, 450)  #크기 비율
        self.setMinimumSize(800, 450)


def main():
    init_db()
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
