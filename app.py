from flask import Flask, jsonify, request, render_template
import pymysql
import os
from dotenv import load_dotenv


# =========================================================
# 환경 변수 및 DB 설정
# =========================================================

# .env 파일의 환경 변수 불러오기
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


# DB 연결 객체 생성
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


# =========================================================
# Flask 앱 설정
# =========================================================

app = Flask(__name__)

# jsonify() 사용 시 한글을 그대로 표시
app.json.ensure_ascii = False


# =========================================================
# 과목 API
# =========================================================

# ---------------------------------------------------------
# 과목 목록 조회
# GET /api/subjects
# ---------------------------------------------------------
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    conn = None
    cur = None

    try:
        conn = get_connection()

        # 조회 결과를 딕셔너리 형태로 받기 위해 DictCursor 사용
        cur = conn.cursor(pymysql.cursors.DictCursor)

        cur.execute('SELECT * FROM subject')
        subjects = cur.fetchall()

        return jsonify(subjects)

    except pymysql.MySQLError as e:
        print(e)

        return jsonify({
            'message': 'get_subjects() DB 처리 실패'
        }), 500

    finally:
        # 오류 발생 여부와 관계없이 DB 연결 정리
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 과목 등록
# POST /api/subjects
# ---------------------------------------------------------
@app.route('/api/subjects', methods=['POST'])
def create_subject():
    conn = None
    cur = None

    try:
        # 클라이언트가 보낸 JSON 데이터 받기
        # JSON 형식이 아니면 에러 대신 None 반환
        data = request.get_json(silent=True)

        # 요청 데이터 자체가 없는 경우
        if data is None:
            return jsonify({
                'message': '요청 데이터가 없습니다.'
            }), 400

        # name 항목이 없는 경우
        if 'name' not in data:
            return jsonify({
                'message': 'name이 존재하지 않습니다.'
            }), 400

        subject_name = data['name']

        # 과목명이 비어 있는 경우
        if subject_name is None or subject_name == '':
            return jsonify({
                'message': '과목명을 입력해주세요.'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # 같은 이름의 과목이 이미 존재하는지 확인
        cur.execute(
            'SELECT * FROM subject WHERE name = %s',
            (subject_name,)
        )

        subject = cur.fetchone()

        if subject is not None:
            return jsonify({
                'message': '이미 존재하는 과목입니다.'
            }), 409

        # 새로운 과목 등록
        cur.execute(
            '''
            INSERT INTO subject(name)
            VALUES (%s)
            ''',
            (subject_name,)
        )

        # DB 변경사항 확정
        conn.commit()

        return jsonify({
            'message': '과목 등록 성공',
            'subject': data
        }), 201

    except pymysql.MySQLError as e:
        # DB 작업 중 오류가 발생하면 변경사항 취소
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'create_subject() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 과목 수정
# PUT /api/subjects/<subject_id>
# ---------------------------------------------------------
@app.route('/api/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    conn = None
    cur = None

    try:
        # 수정할 JSON 데이터 받기
        data = request.get_json(silent=True)

        # 요청 데이터 자체가 없는 경우
        if data is None:
            return jsonify({
                'message': '요청 데이터가 없습니다.'
            }), 400

        # name 항목이 없는 경우
        if 'name' not in data:
            return jsonify({
                'message': 'name이 존재하지 않습니다.'
            }), 400

        subject_name = data['name']

        # 과목명이 비어 있는 경우
        if subject_name is None or subject_name == '':
            return jsonify({
                'message': '과목명을 입력해주세요.'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # 수정하려는 과목이 실제로 존재하는지 확인
        cur.execute(
            'SELECT * FROM subject WHERE id = %s',
            (subject_id,)
        )

        subject = cur.fetchone()

        if subject is None:
            return jsonify({
                'message': '해당 과목이 없습니다.'
            }), 404

        # 다른 과목이 같은 이름을 사용하고 있는지 확인
        # 현재 수정 중인 과목의 id는 검사 대상에서 제외
        cur.execute(
            '''
            SELECT *
            FROM subject
            WHERE name = %s
              AND id != %s
            ''',
            (subject_name, subject_id)
        )

        duplicate_subject = cur.fetchone()

        if duplicate_subject is not None:
            return jsonify({
                'message': '이미 존재하는 과목입니다.'
            }), 409

        # 과목명 수정
        cur.execute(
            '''
            UPDATE subject
            SET name = %s
            WHERE id = %s
            ''',
            (subject_name, subject_id)
        )

        conn.commit()

        return jsonify({
            'message': '과목 수정 성공',
            'subject': data
        }), 200

    except pymysql.MySQLError as e:
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'update_subject() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 과목 삭제
# DELETE /api/subjects/<subject_id>
# ---------------------------------------------------------
@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        # 삭제하려는 과목이 실제로 존재하는지 확인
        cur.execute(
            'SELECT * FROM subject WHERE id = %s',
            (subject_id,)
        )

        subject = cur.fetchone()

        if subject is None:
            return jsonify({
                'message': '해당 과목이 없습니다.'
            }), 404

        # 해당 과목을 사용하고 있는 공부 기록 개수 확인
        cur.execute(
            '''
            SELECT COUNT(*)
            FROM study
            WHERE subject_id = %s
            ''',
            (subject_id,)
        )

        # fetchone() 결과는 (개수,) 형태의 튜플이므로
        # [0]을 사용해 실제 숫자만 꺼냄
        count = cur.fetchone()[0]

        # 사용 중인 과목이면 삭제하지 않음
        if count > 0:
            return jsonify({
                'message': '사용 중인 과목은 삭제할 수 없습니다.'
            }), 409

        # 사용 중이 아닌 과목 삭제
        cur.execute(
            '''
            DELETE FROM subject
            WHERE id = %s
            ''',
            (subject_id,)
        )

        conn.commit()

        return jsonify({
            'message': '과목 삭제 성공',
            'subject': subject_id
        }), 200

    except pymysql.MySQLError as e:
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'delete_subject() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# =========================================================
# 공부 기록 API
# =========================================================

# ---------------------------------------------------------
# 공부 기록 목록 조회
# GET /api/studies
# ---------------------------------------------------------
@app.route('/api/studies', methods=['GET'])
def get_studies():
    conn = None
    cur = None

    try:
        conn = get_connection()

        # 조회 결과를 딕셔너리 형태로 반환
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # study의 subject_id와 subject의 id를 연결해서
        # 과목 id 대신 과목 이름을 반환
        cur.execute(
            '''
            SELECT
                study.id,
                subject.name AS subject,
                study.study_date,
                study.study_minute,
                study.content
            FROM study
            JOIN subject
                ON study.subject_id = subject.id
            ORDER BY study.study_date DESC
            '''
        )

        studies = cur.fetchall()

        return jsonify(studies)

    except pymysql.MySQLError as e:
        print(e)

        return jsonify({
            'message': 'get_studies() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 공부 기록 등록
# POST /api/studies
# ---------------------------------------------------------
@app.route('/api/studies', methods=['POST'])
def create_study():
    conn = None
    cur = None

    try:
        # 클라이언트가 보낸 JSON 데이터 받기
        data = request.get_json(silent=True)

        # 요청 데이터 자체가 없는 경우
        if data is None:
            return jsonify({
                'message': '요청 데이터가 없습니다.'
            }), 400

        # 공부 기록 등록에 필요한 필수 항목 확인
        if (
            'subject_id' not in data
            or 'study_date' not in data
            or 'study_minute' not in data
        ):
            return jsonify({
                'message': '필수 입력값이 없습니다.'
            }), 400

        subject_id = data['subject_id']
        study_date = data['study_date']
        study_minute = data['study_minute']

        # content는 선택값
        # 없으면 None으로 저장
        content = data.get('content')

        # 공부 시간은 정수이며 0보다 커야 함
        if not isinstance(study_minute, int) or study_minute <= 0:
            return jsonify({
                'message': '공부 시간은 0보다 큰 정수여야 합니다.'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # 전달받은 subject_id가 실제 과목인지 확인
        cur.execute(
            'SELECT * FROM subject WHERE id = %s',
            (subject_id,)
        )

        subject = cur.fetchone()

        if subject is None:
            return jsonify({
                'message': '해당 과목이 없습니다.'
            }), 404

        # 공부 기록 등록
        cur.execute(
            '''
            INSERT INTO study(
                subject_id,
                study_date,
                study_minute,
                content
            )
            VALUES (%s, %s, %s, %s)
            ''',
            (
                subject_id,
                study_date,
                study_minute,
                content
            )
        )

        conn.commit()

        return jsonify({
            'message': '공부 등록 성공',
            'study': data
        }), 201

    except pymysql.MySQLError as e:
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'create_study() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 공부 기록 수정
# PUT /api/studies/<study_id>
# ---------------------------------------------------------
@app.route('/api/studies/<int:study_id>', methods=['PUT'])
def update_study(study_id):
    conn = None
    cur = None

    try:
        # 수정할 JSON 데이터 받기
        data = request.get_json(silent=True)

        # 요청 데이터 자체가 없는 경우
        if data is None:
            return jsonify({
                'message': '요청 데이터가 없습니다.'
            }), 400

        # 공부 기록 수정에 필요한 필수 항목 확인
        if (
            'subject_id' not in data
            or 'study_date' not in data
            or 'study_minute' not in data
        ):
            return jsonify({
                'message': '필수 입력값이 없습니다.'
            }), 400

        subject_id = data['subject_id']
        study_date = data['study_date']
        study_minute = data['study_minute']

        # content는 선택값
        content = data.get('content')

        # 공부 시간은 정수이며 0보다 커야 함
        if not isinstance(study_minute, int) or study_minute <= 0:
            return jsonify({
                'message': '공부 시간은 0보다 큰 정수여야 합니다.'
            }), 400

        conn = get_connection()
        cur = conn.cursor()

        # 수정하려는 공부 기록이 실제로 존재하는지 확인
        cur.execute(
            'SELECT * FROM study WHERE id = %s',
            (study_id,)
        )

        study = cur.fetchone()

        if study is None:
            return jsonify({
                'message': '해당 공부기록이 없습니다.'
            }), 404

        # 전달받은 subject_id가 실제 과목인지 확인
        cur.execute(
            'SELECT * FROM subject WHERE id = %s',
            (subject_id,)
        )

        subject = cur.fetchone()

        if subject is None:
            return jsonify({
                'message': '해당 과목이 없습니다.'
            }), 404

        # 공부 기록 수정
        cur.execute(
            '''
            UPDATE study
            SET subject_id = %s,
                study_date = %s,
                study_minute = %s,
                content = %s
            WHERE id = %s
            ''',
            (
                subject_id,
                study_date,
                study_minute,
                content,
                study_id
            )
        )

        conn.commit()

        return jsonify({
            'message': '공부 수정 성공',
            'study': data
        }), 200

    except pymysql.MySQLError as e:
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'update_study() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# 공부 기록 삭제
# DELETE /api/studies/<study_id>
# ---------------------------------------------------------
@app.route('/api/studies/<int:study_id>', methods=['DELETE'])
def delete_study(study_id):
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        # 삭제하려는 공부 기록이 실제로 존재하는지 확인
        cur.execute(
            'SELECT * FROM study WHERE id = %s',
            (study_id,)
        )

        study = cur.fetchone()

        if study is None:
            return jsonify({
                'message': '해당 공부기록이 없습니다.'
            }), 404

        # 공부 기록 삭제
        cur.execute(
            '''
            DELETE FROM study
            WHERE id = %s
            ''',
            (study_id,)
        )

        conn.commit()

        return jsonify({
            'message': '공부 삭제 성공',
            'study': study_id
        }), 200

    except pymysql.MySQLError as e:
        if conn is not None:
            conn.rollback()

        print(e)

        return jsonify({
            'message': 'delete_study() DB 처리 실패'
        }), 500

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()


# =========================================================
# 기본 페이지
# =========================================================

@app.route('/')
def index():
    return render_template('index.html')


# 현재 파일을 직접 실행했을 때 Flask 서버 시작
if __name__ == '__main__':
    app.run(debug=True)