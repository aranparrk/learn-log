from flask import Flask
import pymysql
import os
from dotenv import load_dotenv

# .env 읽기
load_dotenv()

# DB 연결 정보
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# DB 연결 함수
def get_connection():
    if DB_PASSWORD is None:
        raise ValueError('DB_PASSWORD가 세팅 되지 않았습니다.')

    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Flask 앱 실행
app = Flask(__name__)

# 기본 라우트
@app.route('/')
def index():
    return 'LearnLog 서버 실행 성공!'

if __name__ == '__main__':
    app.run(debug=True)