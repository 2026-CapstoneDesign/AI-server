from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel  
import shutil
import os

from extractor import extract_text
from ai import summarize, ask_chatbot 
from generator import generate_content, generate_quiz, generate_recommendations

app = FastAPI()


class AskRequest(BaseModel):
    question: str
    manual_text: str


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
        
        # 7. 챗봇용 알바생 맞춤형 추천 질문 8개 생성
        recommendations = generate_recommendations(summary)

        # 8. 최종 결과 반환
        return {
            "summary": summary,
            "content": content,
            "quiz": quiz,
            "recommendations": recommendations
        }

    except ValueError as ve:
        return {"error": str(ve)}

    except Exception as e:
        return {"error": f"서버 오류: {str(e)}"}

    finally:
        
        if os.path.exists(file_path):
            os.remove(file_path)


# ==========================================================
# 챗봇 실시간 질문 처리 라우터 (POST /ask) 
# ==========================================================
@app.post("/ask")
async def ask(payload: AskRequest):
    try:
        
        answer = ask_chatbot(payload.question, payload.manual_text)
        return {"answer": answer}
    except Exception as e:
        return {"error": f"AI 답변 생성 중 오류 발생: {str(e)}"}