from fastapi import FastAPI, UploadFile, File
import shutil
import os

from extractor import extract_text
from ai import summarize
from generator import generate_content, generate_quiz

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI server running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    try:
        # 1. 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. 텍스트 추출
        text = extract_text(file_path, file.filename)

        if not text or len(text.strip()) == 0:
            return {"error": "텍스트를 추출할 수 없습니다."}

        # 3. 길이 제한 (안정성)
        text = text[:3000]

        # 4. 요약
        summary = summarize(text)

        # 5. 콘텐츠 생성
        content = generate_content(summary)

        # 6. 퀴즈 생성
        quiz = generate_quiz(summary)

        return {
            "summary": summary,
            "content": content,
            "quiz": quiz
        }

    except ValueError as ve:
        return {"error": str(ve)}

    except Exception as e:
        return {"error": f"서버 오류: {str(e)}"}

    finally:
        # 7. 임시 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)