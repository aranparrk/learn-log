# 📚 LearnLog

개인 공부 기록을 관리하기 위한 웹 애플리케이션입니다.

공부한 날짜, 과목, 공부 시간, 학습 내용을 기록하고  
대시보드에서 전체 학습 현황과 과목별 공부 시간을 확인할 수 있습니다.

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### Backend
- Python
- Flask

### Database
- MySQL
- PyMySQL

### ETC
- Git
- GitHub

---

## ✨ 주요 기능

### 1. 공부 기록 관리

- 공부 기록 조회
- 공부 기록 등록
- 공부 기록 수정
- 공부 기록 삭제
- 최근 공부 날짜 및 등록 순서 기준 정렬

공부 기록에는 다음 정보가 저장됩니다.

- 공부 날짜
- 과목
- 공부 시간
- 공부 내용

---

### 2. 과목 관리

- 과목 조회
- 과목 추가
- 과목 수정
- 과목 삭제

공부 기록에서 사용 중인 과목은 삭제할 수 없도록 처리했습니다.

---

### 3. 대시보드

학습 데이터를 기반으로 다음 정보를 확인할 수 있습니다.

- 오늘 공부 시간
- 이번 주 공부 시간
- 총 공부 시간
- 과목별 누적 공부 시간

과목별 공부 시간은 막대그래프로 표시되며  
가장 많이 공부한 과목을 기준으로 상대적인 길이를 계산합니다.

---

### 4. 다크모드

- 라이트모드 / 다크모드 전환
- 현재 모드에 따라 버튼 문구 변경
- `sessionStorage`를 이용해 새로고침 후에도 현재 테마 유지

브라우저 탭을 닫으면 저장된 테마 정보는 초기화됩니다.

---

## 🗂 프로젝트 구조
```text
learn-log/

├── app.py  
├── schema.sql  
├── templates/  
│   └── index.html  
├── static/  
│   ├── css/  
│   │   └── style.css  
│   └── js/  
│       └── app.js  
└── README.md  
```
---

## 🗄 Database

### subject

과목 정보를 저장하는 테이블입니다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| id | INT | 과목 ID |
| name | VARCHAR(50) | 과목명 |

`name`은 중복 등록을 방지하기 위해 `UNIQUE`로 설정했습니다.

### study

공부 기록을 저장하는 테이블입니다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| id | INT | 공부 기록 ID |
| subject_id | INT | 과목 ID |
| study_date | DATE | 실제 공부 날짜 |
| study_minute | INT | 공부 시간(분) |
| content | VARCHAR(200) | 공부 내용 |
| created_at | DATETIME | 기록 등록 시간 |

`study.subject_id`는 `subject.id`를 참조하는 외래키입니다.

`study_date`는 실제 공부한 날짜를 저장하고,  
`created_at`은 기록이 등록된 시간을 저장합니다.

---

## 🔌 API

### 과목

| Method | URL | 기능 |
| --- | --- | --- |
| GET | `/api/subjects` | 과목 목록 조회 |
| POST | `/api/subjects` | 과목 추가 |
| PUT | `/api/subjects/<subject_id>` | 과목 수정 |
| DELETE | `/api/subjects/<subject_id>` | 과목 삭제 |

### 공부 기록

| Method | URL | 기능 |
| --- | --- | --- |
| GET | `/api/studies` | 공부 기록 조회 |
| POST | `/api/studies` | 공부 기록 등록 |
| PUT | `/api/studies/<study_id>` | 공부 기록 수정 |
| DELETE | `/api/studies/<study_id>` | 공부 기록 삭제 |

### 대시보드

| Method | URL | 기능 |
| --- | --- | --- |
| GET | `/api/dashboard` | 공부 시간 통계 조회 |

대시보드 API에서는 다음 데이터를 반환합니다.

- 오늘 공부 시간
- 이번 주 공부 시간
- 전체 공부 시간
- 과목별 누적 공부 시간

---

## 🔄 데이터 흐름

사용자가 화면에서 데이터를 입력하거나 버튼을 클릭하면 다음 순서로 처리됩니다.

JavaScript  
→ Flask API 요청  
→ MySQL 조회 / 저장 / 수정 / 삭제  
→ Flask JSON 응답  
→ JavaScript 화면 갱신

공부 기록 또는 과목 데이터가 변경되면 필요한 목록과 대시보드를 다시 조회하여 페이지 새로고침 없이 화면에 반영합니다.

---

## ▶️ 실행 방법

### 1. Repository Clone

```bash
git clone https://github.com/aranparrk/learn-log.git
```

### 2. 필요한 라이브러리 설치

```bash
pip install flask pymysql python-dotenv
```

### 3. MySQL 데이터베이스 준비

프로젝트의 `schema.sql`을 실행하여 테이블을 생성합니다.

### 4. DB 접속 정보 설정

로컬 MySQL 환경에 맞게 데이터베이스 접속 정보를 설정합니다.

비밀번호나 API Key와 같은 민감한 정보는 `.env` 파일에서 관리하고 Git에 업로드하지 않습니다.

### 5. Flask 실행

```bash
python app.py
```

실행 후 브라우저에서 Flask 서버 주소로 접속합니다.

---

## 💡 구현하면서 학습한 내용

- Flask를 이용한 REST API 구현
- MySQL과 Python 연동
- CRUD 처리 흐름
- 외래키를 이용한 테이블 관계 설정
- JavaScript `fetch()`를 이용한 API 통신
- JSON 데이터 송수신
- DOM을 이용한 동적 HTML 생성
- GET / POST / PUT / DELETE 요청 처리
- JavaScript에서 등록 상태와 수정 상태 관리
- SQL `SUM`, `GROUP BY`, `LEFT JOIN`을 이용한 데이터 집계
- 데이터베이스 값을 이용한 동적 막대그래프 구현
- `sessionStorage`를 이용한 화면 상태 유지

---

## 📌 Version

### v1

- 공부 기록 CRUD
- 과목 CRUD
- 학습 통계 대시보드
- 과목별 공부 시간 그래프
- 다크모드
- 세션 기반 테마 유지

---

## 👩‍💻 Author

**aranparrk**

© 2026 LearnLog by aranparrk.
