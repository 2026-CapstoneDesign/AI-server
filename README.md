# AI 기반 아르바이트 교육 서비스 (AI Server)

## 프로젝트 소개
<img width="7680" height="3840" alt="Group 149" src="https://github.com/user-attachments/assets/337c6011-c353-49e5-b843-ebaa1565bf19" />
프로젝트 'E:ON(이어온)'은 AI 기반 아르바이트 교육 및 매뉴얼 학습 플랫폼입니다.

AI Server는 교육 매뉴얼을 분석하여 학습 콘텐츠를 자동 생성하는 역할을 수행합니다.

PDF 문서에서 텍스트를 추출하고, OpenAI API를 활용하여 매뉴얼 요약 및 퀴즈를 생성하는 AI 서비스 서버입니다.

---

## 🛠️ Tech Stack

* Python
* FastAPI
* OpenAI API
* PDF Parsing
* Uvicorn
* Docker
* AWS EC2

---

## 🏗️ AI Architecture

```text
Manual Upload (PDF or Text)
        ↓
PDF Text Extraction
        ↓
OpenAI API
        ↓
Summary Generation
        ↓
Quiz Generation
        ↓
Backend Server
```

---

## 📂 주요 기능

### 📄 PDF 분석

* PDF 파일 업로드
* 텍스트 추출
* 전처리 및 분석

### 🧠 AI 요약 생성

* 매뉴얼 자동 요약
* 핵심 개념 추출
* 학습용 콘텐츠 생성

### ❓ AI 퀴즈 생성

* 객관식 문제 생성
* 정답 및 해설 생성
* 교육용 평가 콘텐츠 생성

---

## 👨‍💻 담당자

### 임하리

#### AI 서버 구축 및 배포

* FastAPI 서버 구축
* Docker 기반 배포 환경 구성
* AWS 서버 배포

#### AI 학습 콘텐츠 생성

* 매뉴얼 요약(Summarize) 기능 구현
* AI 퀴즈 생성 기능 구현
* OpenAI API 연동

---

## 📡 주요 API

### 매뉴얼 요약

```http
POST /summarize
```

### 퀴즈 생성

```http
POST /generate-quiz
```

---

## 🚀 Run

### Local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker

```bash
docker build -t ai-server .
docker run -p 8000:8000 ai-server
```

---

## 👥 Team

2026 Capstone Design Team
