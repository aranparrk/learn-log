from flask import Flask, jsonify, request
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

# JSON 한글 표시 설정
app.json.ensure_ascii = False

# 과목 목록 조회 함수
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM subject')

    subjects = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(subjects)

# 공부 목록 조회 함수
@app.route('/api/studies', methods=['GET'])
def get_studies():
    conn = get_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            study.id,
            subject.name AS subject,
            study.study_date,
            study.study_minute,
            study.content
        FROM study
        JOIN subject
            ON study.subject_id = subject.id
    """)

    studies = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(studies)

# 과목 등록 함수
@app.route('/api/subjects', methods=['POST'])
def create_subject():
    data = request.get_json()

    subject_name = data['name']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        INSERT INTO subject(name)
        VALUES (%s)
        ''',
        (subject_name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'message' : '등록성공',
        'subject': data
    }), 201

# 공부 등록 함수
@app.route('/api/studies', methods=['POST'])
def create_study():
    data = request.get_json()

    subject_id = data['subject_id']
    study_date = data['study_date']
    study_minute = data['study_minute']
    content = data['content']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
            INSERT INTO study(subject_id, study_date, study_minute, content)
            VALUES (%s, %s, %s, %s)
        ''',
        (subject_id, study_date, study_minute, content)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'message': '등록성공',
        'study': data
    }), 201

# 공부 목록 삭제
@app.route('/api/studies/<int:study_id>', methods=['DELETE'])
def delete_study(study_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
            DELETE FROM study WHERE id = %s
        ''',
        (study_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'message' : '삭제 성공',
        'study': study_id
    }), 200

# 공부 목록 수정
@app.route('/api/studies/<int:study_id>', methods=['PUT'])
def update_study(study_id):
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    subject_id = data['subject_id']
    study_date = data['study_date']
    study_minute = data['study_minute']
    content = data['content']

    cur.execute(
        '''
            UPDATE study SET subject_id = %s, study_date = %s, study_minute = %s, content = %s WHERE id = %s
        ''',
        (subject_id, study_date, study_minute, content, study_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'message' : '수정 성공',
        'study': data
    }), 200

# 기본 라우트
@app.route('/')
def index():
    return 'LearnLog 서버 실행 성공!'

if __name__ == '__main__':
    app.run(debug=True)