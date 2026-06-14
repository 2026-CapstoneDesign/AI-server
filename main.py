from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import shutil
import os
import json

load_dotenv()

from extractor import extract_text
from ai import summarize
from generator import generate_content, generate_quiz

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class QuizGenerateRequest(BaseModel):
    summary: str
    quiz_count: int = 5


class AskRequest(BaseModel):
    question: str
    manual_text: str


def parse_json_safely(value):
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {"raw": value, "error": "AI 응답을 JSON으로 파싱하지 못했습니다."}


@app.get("/")
def root():
    return {"message": "AI server running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        text = extract_text(file_path, file.filename)
        if not text or len(text.strip()) == 0:
            return {"success": False, "error": "텍스트를 추출할 수 없습니다."}
        text = text[:3000]
        summary = summarize(text)
        content = generate_content(summary)
        quiz = generate_quiz(summary)
        return {
            "success": True,
            "summary": parse_json_safely(summary),
            "content": parse_json_safely(content),
            "quiz": parse_json_safely(quiz)
        }
    except Exception as e:
        return {"success": False, "error": f"서버 오류: {str(e)}"}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/ask")
def ask(req: AskRequest):
    try:
        prompt = f"""
다음 매장 매뉴얼을 기반으로 알바생의 질문에 답변해라.

매뉴얼 내용:
{req.manual_text[:2000]}

알바생 질문: {req.question}

조건:
- 매뉴얼에 있는 내용이면 친절하게 답변해라.
- 매뉴얼에 없는 내용이면 "죄송해요, 매뉴얼에 없는 내용이에요. 사장님께 직접 여쭤보세요!" 라고 답변해라.
- 답변은 짧고 명확하게 해라.
"""
        res = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = res.choices[0].message.content

        actions = []
        if "사장님께 직접" in answer or "매뉴얼에 없는" in answer:
            actions.append("post_board")

        return {"success": True, "answer": answer, "actions": actions}
    except Exception as e:
        return {"success": False, "error": f"답변 생성 중 오류 발생: {str(e)}"}


@app.post("/quiz/generate")
def quiz_generate(req: QuizGenerateRequest):
    try:
        if not req.summary or len(req.summary.strip()) < 10:
            return {"success": False, "error": "퀴즈를 생성할 요약 내용이 부족합니다."}
        summary = req.summary[:3000]
        quiz = generate_quiz(summary)
        return {"success": True, "quiz": parse_json_safely(quiz)}
    except Exception as e:
        return {"success": False, "error": f"퀴즈 생성 중 오류 발생: {str(e)}"}