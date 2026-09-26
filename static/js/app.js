// 다크모드

const themeButton = document.getElementById("theme-toggle");

themeButton.addEventListener("click", function () {
  document.body.classList.toggle("dark");
});

// 공부 기록 조회
const studyList = document.getElementById("study-list");

fetch("/api/studies")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    const study = data[0];

    for (let i = 0; i < data.length; i++) {
      const study = data[i];
      const date = new Date(study.study_date);

      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");

      const formattedDate = `${year}-${month}-${day}`;

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
