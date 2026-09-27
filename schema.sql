-- LearnLog Database Schema

-- 외래키 때문에 study 테이블부터 삭제
DROP TABLE IF EXISTS study;
DROP TABLE IF EXISTS subject;


-- =========================================
-- 과목 테이블
-- =========================================

CREATE TABLE subject (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);


-- =========================================
-- 공부 기록 테이블
-- =========================================

CREATE TABLE study (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject_id INT NOT NULL,
    study_date DATE NOT NULL,
    study_minute INT NOT NULL,
    content VARCHAR(200),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_study_subject
        FOREIGN KEY (subject_id)
        REFERENCES subject(id)
);