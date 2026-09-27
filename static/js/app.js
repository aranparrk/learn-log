// =========================================================
// HTML 요소 가져오기
// =========================================================

// 다크모드
const themeButton = document.getElementById("theme-toggle");

// 공부 기록
const studyList = document.getElementById("study-list");

const studyDate = document.getElementById("study-date");
const studySubject = document.getElementById("study-subject");
const studyMinute = document.getElementById("study-minute");
const studyContent = document.getElementById("study-content");
const studySubmit = document.getElementById("study-submit");

// 과목 관리
const subjectList = document.getElementById("subject-list");
const subjectName = document.getElementById("subject-name");
const subjectSubmit = document.getElementById("subject-submit");
const subjectCancel = document.getElementById("subject-cancel");

// 대시보드
const todayStudyTime = document.getElementById("today-study-time");

const weekStudyTime = document.getElementById("week-study-time");

const totalStudyTime = document.getElementById("total-study-time");

const subjectChart = document.getElementById("subject-chart");

// =========================================================
// 수정 상태 저장
// =========================================================

// 공부 기록 수정 중인 id
// null이면 등록 상태
let editingStudyId = null;

// 과목 수정 중인 id
// null이면 추가 상태
let editingSubjectId = null;

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
      studyList.innerHTML = "";

      // 공부 기록이 없을 경우
      if (data.length === 0) {
        studyList.innerHTML = `
                    <p>등록된 공부 기록이 없습니다.</p>
                `;

        return;
      }

      // ---------------------------------------------
      // 공부 기록 화면 출력
      // ---------------------------------------------

      for (let i = 0; i < data.length; i++) {
        const study = data[i];

        // 날짜 형식 변경
        const date = new Date(study.study_date);

        const year = date.getFullYear();

        const month = String(date.getMonth() + 1).padStart(2, "0");

        const day = String(date.getDate()).padStart(2, "0");

        const formattedDate = `${year}-${month}-${day}`;

        studyList.innerHTML += `
                    <div class="study-item">

                        <div class="study-info">

                            <strong>
                                ${study.subject}
                            </strong>

                            <span>
                                ${formattedDate}
                            </span>

                        </div>


                        <p>
                            ${study.content}
                        </p>


                        <div class="study-footer">

                            <span>
                                ${study.study_minute}분
                            </span>

                            <div>

                                <button
                                    class="edit-button"
                                    data-id="${study.id}"
                                >
                                    수정
                                </button>

                                <button
                                    class="delete-button"
                                    data-id="${study.id}"
                                >
                                    삭제
                                </button>

                            </div>

                        </div>

                    </div>
                `;
      }

      // ---------------------------------------------
      // 공부 기록 삭제
      // ---------------------------------------------

      const deleteButtons = studyList.querySelectorAll(".delete-button");

      for (let i = 0; i < deleteButtons.length; i++) {
        const button = deleteButtons[i];

        button.addEventListener("click", function () {
          const studyId = Number(button.dataset.id);

          fetch(`/api/studies/${studyId}`, {
            method: "DELETE",
          })
            .then(function (response) {
              return response.json();
            })

            .then(function (data) {
              console.log(data);

              loadStudies();

              loadDashboard();
            });
        });
      }

      // ---------------------------------------------
      // 공부 기록 수정 버튼
      // ---------------------------------------------

      const editButtons = studyList.querySelectorAll(".edit-button");

      for (let i = 0; i < editButtons.length; i++) {
        const button = editButtons[i];

        button.addEventListener("click", function () {
          const studyId = Number(button.dataset.id);

          // 수정 상태로 변경
          editingStudyId = studyId;

          studySubmit.textContent = "수정 저장";

          // 클릭한 공부 기록 찾기
          for (let j = 0; j < data.length; j++) {
            const study = data[j];

            if (study.id === studyId) {
              const date = new Date(study.study_date);

              const year = date.getFullYear();

              const month = String(date.getMonth() + 1).padStart(2, "0");

              const day = String(date.getDate()).padStart(2, "0");

              const formattedDate = `${year}-${month}-${day}`;

              studyDate.value = formattedDate;

              studySubject.value = study.subject_id;

              studyMinute.value = study.study_minute;

              studyContent.value = study.content;

              break;
            }
          }
        });
      }
    });
}

// =========================================================
// 공부 기록 입력폼 초기화
// =========================================================

function resetStudyForm() {
  studyDate.value = "";

  studyMinute.value = "";

  studyContent.value = "";

  editingStudyId = null;

  studySubmit.textContent = "등록";
}

// =========================================================
// 공부 기록 등록 / 수정
// =========================================================

studySubmit.addEventListener("click", function () {
  const studyData = {
    subject_id: Number(studySubject.value),

    study_date: studyDate.value,

    study_minute: Number(studyMinute.value),

    content: studyContent.value,
  };

  // ---------------------------------------------
  // 공부 기록 등록
  // ---------------------------------------------

  if (editingStudyId === null) {
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

        loadStudies();

        loadDashboard();

        resetStudyForm();
      });
  }

  // ---------------------------------------------
  // 공부 기록 수정
  // ---------------------------------------------
  else {
    fetch(`/api/studies/${editingStudyId}`, {
      method: "PUT",

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

        loadStudies();

        loadDashboard();

        resetStudyForm();
      });
  }
});

// =========================================================
// 과목 목록 조회
// =========================================================

function loadSubjects() {
  fetch("/api/subjects")
    .then(function (response) {
      return response.json();
    })

    .then(function (data) {
      // ---------------------------------------------
      // 공부 기록 select 갱신
      // ---------------------------------------------

      studySubject.innerHTML = "";

      for (let i = 0; i < data.length; i++) {
        const subject = data[i];

        const option = document.createElement("option");

        option.value = subject.id;

        option.textContent = subject.name;

        studySubject.appendChild(option);
      }

      // ---------------------------------------------
      // 과목 관리 목록 갱신
      // ---------------------------------------------

      subjectList.innerHTML = "";

      if (data.length === 0) {
        subjectList.innerHTML = `
                    <p>등록된 과목이 없습니다.</p>
                `;
      }

      for (let i = 0; i < data.length; i++) {
        const subject = data[i];

        subjectList.innerHTML += `
                    <div class="subject-item">

                        <span>
                            ${subject.name}
                        </span>

                        <div>

                            <button
                                class="subject-edit-button"
                                data-id="${subject.id}"
                            >
                                수정
                            </button>

                            <button
                                class="delete-button subject-delete-button"
                                data-id="${subject.id}"
                            >
                                삭제
                            </button>

                        </div>

                    </div>
                `;
      }

      // ---------------------------------------------
      // 과목 수정 버튼
      // ---------------------------------------------

      const subjectEditButtons = subjectList.querySelectorAll(".subject-edit-button");

      for (let i = 0; i < subjectEditButtons.length; i++) {
        const button = subjectEditButtons[i];

        button.addEventListener("click", function () {
          const subjectId = Number(button.dataset.id);

          editingSubjectId = subjectId;

          subjectSubmit.textContent = "수정 저장";

          subjectCancel.hidden = false;

          for (let j = 0; j < data.length; j++) {
            const subject = data[j];

            if (subject.id === subjectId) {
              subjectName.value = subject.name;

              break;
            }
          }
        });
      }

      // ---------------------------------------------
      // 과목 삭제 버튼
      // ---------------------------------------------

      const subjectDeleteButtons = subjectList.querySelectorAll(".subject-delete-button");

      for (let i = 0; i < subjectDeleteButtons.length; i++) {
        const button = subjectDeleteButtons[i];

        button.addEventListener("click", function () {
          const subjectId = Number(button.dataset.id);

          fetch(`/api/subjects/${subjectId}`, {
            method: "DELETE",
          })
            .then(function (response) {
              return response.json().then(function (data) {
                return {
                  ok: response.ok,

                  data: data,
                };
              });
            })

            .then(function (result) {
              if (!result.ok) {
                alert(result.data.message);

                return;
              }

              console.log(result.data);

              loadSubjects();

              loadDashboard();

              resetSubjectForm();
            });
        });
      }
    });
}

// =========================================================
// 과목 입력폼 초기화
// =========================================================

function resetSubjectForm() {
  subjectName.value = "";

  editingSubjectId = null;

  subjectSubmit.textContent = "추가";

  subjectCancel.hidden = true;
}

// =========================================================
// 과목 추가 / 수정
// =========================================================

subjectSubmit.addEventListener("click", function () {
  const name = subjectName.value.trim();

  if (name === "") {
    alert("과목명을 입력해주세요.");

    return;
  }

  const subjectData = {
    name: name,
  };

  // ---------------------------------------------
  // 과목 추가
  // ---------------------------------------------

  if (editingSubjectId === null) {
    fetch("/api/subjects", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(subjectData),
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return {
            ok: response.ok,

            data: data,
          };
        });
      })

      .then(function (result) {
        if (!result.ok) {
          alert(result.data.message);

          return;
        }

        console.log(result.data);

        resetSubjectForm();

        loadSubjects();

        loadDashboard();
      });
  }

  // ---------------------------------------------
  // 과목 수정
  // ---------------------------------------------
  else {
    fetch(`/api/subjects/${editingSubjectId}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(subjectData),
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return {
            ok: response.ok,

            data: data,
          };
        });
      })

      .then(function (result) {
        if (!result.ok) {
          alert(result.data.message);

          return;
        }

        console.log(result.data);

        resetSubjectForm();

        loadSubjects();

        loadStudies();

        loadDashboard();
      });
  }
});

// =========================================================
// 과목 수정 취소
// =========================================================

subjectCancel.addEventListener("click", function () {
  resetSubjectForm();
});

// =========================================================
// 대시보드 조회
// =========================================================

function loadDashboard() {
  fetch("/api/dashboard")
    .then(function (response) {
      return response.json();
    })

    .then(function (data) {
      // ---------------------------------------------
      // 공부 시간 카드
      // ---------------------------------------------

      todayStudyTime.textContent = `${data.today}분`;

      weekStudyTime.textContent = `${data.week}분`;

      totalStudyTime.textContent = `${data.total}분`;

      // ---------------------------------------------
      // 과목별 그래프 초기화
      // ---------------------------------------------

      subjectChart.innerHTML = "";

      // ---------------------------------------------
      // 가장 공부 시간이 긴 과목 찾기
      // ---------------------------------------------

      let maxMinute = 0;

      for (let i = 0; i < data.subjects.length; i++) {
        // MySQL 결과가 문자열일 수 있어서
        // 숫자로 변환
        const minute = Number(data.subjects[i].study_minute);

        if (minute > maxMinute) {
          maxMinute = minute;
        }
      }

      // ---------------------------------------------
      // 과목별 그래프 생성
      // ---------------------------------------------

      for (let i = 0; i < data.subjects.length; i++) {
        const subject = data.subjects[i];

        const minute = Number(subject.study_minute);

        let width = 0;

        if (maxMinute > 0) {
          width = (minute / maxMinute) * 100;
        }

        subjectChart.innerHTML += `
                    <div class="chart-row">

                        <span class="chart-label">
                            ${subject.name}
                        </span>

                        <div class="chart-track">

                            <div
                                class="chart-bar"
                                style="width: ${width}%"
                            ></div>

                        </div>

                        <span class="chart-value">
                            ${minute}분
                        </span>

                    </div>
                `;
      }
    });
}

// =========================================================
// 페이지 처음 열렸을 때 실행
// =========================================================

loadStudies();

loadSubjects();

loadDashboard();
