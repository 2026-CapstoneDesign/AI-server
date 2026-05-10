from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import json

from extractor import extract_text
from ai import summarize
from generator import generate_content, generate_quiz

app = FastAPI()


class QuizGenerateRequest(BaseModel):
    summary: str
    quiz_count: int = 5


def parse_json_safely(value):
    """
    OpenAI 응답이 문자열 JSON으로 올 때 실제 JSON으로 변환하기 위한 함수.
    변환 실패 시 raw 문자열 그대로 반환.
    """
    if isinstance(value, (dict, list)):
        return value

    if not isinstance(value, str):
        return value

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {
            "raw": value,
            "error": "AI 응답을 JSON으로 파싱하지 못했습니다."
        }


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
            return {
                "success": False,
                "error": "텍스트를 추출할 수 없습니다."
            }

        # 3. 길이 제한
        text = text[:3000]

        # 4. 요약 생성
        summary = summarize(text)

        # 5. 카드형 학습 콘텐츠 생성
        content = generate_content(summary)

        # 6. 퀴즈 생성
        quiz = generate_quiz(summary)

        return {
            "success": True,
            "summary": parse_json_safely(summary),
            "content": parse_json_safely(content),
            "quiz": parse_json_safely(quiz)
        }

    except ValueError as ve:
        return {
            "success": False,
            "error": str(ve)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"서버 오류: {str(e)}"
        }

    finally:
        # 7. 임시 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/quiz/generate")
def quiz_generate(req: QuizGenerateRequest):
    try:
        if not req.summary or len(req.summary.strip()) < 10:
            return {
                "success": False,
                "error": "퀴즈를 생성할 요약 내용이 부족합니다."
            }

        summary = req.summary[:3000]

        quiz = generate_quiz(summary)

        return {
            "success": True,
            "quiz": parse_json_safely(quiz)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"퀴즈 생성 중 오류 발생: {str(e)}"
        }