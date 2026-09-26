// =========================================================
// HTML 요소 가져오기
// =========================================================

const themeButton = document.getElementById("theme-toggle");

const studyList = document.getElementById("study-list");

const studyDate = document.getElementById("study-date");
const studySubject = document.getElementById("study-subject");
const studyMinute = document.getElementById("study-minute");
const studyContent = document.getElementById("study-content");
const studySubmit = document.getElementById("study-submit");

// =========================================================
// 다크모드
// =========================================================

themeButton.addEventListener("click", function () {
  document.body.classList.toggle("dark");
});

// =========================================================
// 공부 기록 조회
// =========================================================

function loadStudies() {
  fetch("/api/studies")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // 기존 목록 비우기
      studyList.innerHTML = "";

      // 받아온 공부 기록을 하나씩 화면에 출력
      for (let i = 0; i < data.length; i++) {
        const study = data[i];

        // 날짜 형식 변경
        const date = new Date(study.study_date);

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");

        const formattedDate = `${year}-${month}-${day}`;

        // 공부 기록 화면에 추가
        studyList.innerHTML += `
                    <div class="study-item">

                        <div class="study-info">
                            <strong>${study.subject}</strong>
                            <span>${formattedDate}</span>
                        </div>

                        <p>${study.content}</p>

                        <div class="study-footer">
                            <span>${study.study_minute}분</span>

                            <div>
                                <button>수정</button>
                                <button class="delete-button">삭제</button>
                            </div>
                        </div>

                    </div>
                `;
      }
    });
}

// =========================================================
// 과목 목록 조회
// =========================================================

function loadSubjects() {
  fetch("/api/subjects")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // HTML에 있던 임시 option 제거
      studySubject.innerHTML = "";

      // DB의 과목을 option으로 생성
      for (let i = 0; i < data.length; i++) {
        const subject = data[i];

        const option = document.createElement("option");

        // 실제 값은 subject_id
        option.value = subject.id;

        // 화면에는 과목명 표시
        option.textContent = subject.name;

        studySubject.appendChild(option);
      }
    });
}

// =========================================================
// 공부 기록 등록
// =========================================================

studySubmit.addEventListener("click", function () {
  // 사용자가 입력한 값으로 객체 생성
  const studyData = {
    subject_id: Number(studySubject.value),
    study_date: studyDate.value,
    study_minute: Number(studyMinute.value),
    content: studyContent.value,
  };

  // Flask로 공부 기록 등록 요청
  fetch("/api/studies", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify(studyData),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);

      // 등록 후 공부 기록 다시 조회
      loadStudies();

      // 입력 폼 초기화
      studyDate.value = "";
      studyMinute.value = "";
      studyContent.value = "";
    });
});

// =========================================================
// 페이지가 처음 열렸을 때 실행
// =========================================================

loadStudies();
loadSubjects();
