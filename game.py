from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '048910'
app.config['MYSQL_DB'] = 'SENSELESS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 게임 페이지
@app.route('/game')
def game():
    return render_template('main.html')

# 저장 버튼 처리
@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        # 데이터 추출
        story_key = request.form['story_key']
        story_text = request.form['story_text']
        next_choices = request.form['next_choices']
        found_at = request.form['found_at']

        # stories 테이블에 저장
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stories (story_key, story_text, next_choices) VALUES (%s, %s, %s)", (story_key, story_text, next_choices))
        mysql.connection.commit()

        # treasures 테이블에 저장
        cur.execute("INSERT INTO treasures (found_at) VALUES (%s)", (found_at,))
        mysql.connection.commit()

        cur.close()

        return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True)
