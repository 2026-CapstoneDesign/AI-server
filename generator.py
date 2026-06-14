from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content(summary):
    prompt = f"""
다음 내용을 알바생이 보기 쉬운 카드형 학습 콘텐츠로 만들어라.
반드시 JSON 배열만 반환해라.

JSON 형식:
[{{"title": "제목", "content": "내용"}}]

요약 내용:
{summary}
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

def generate_quiz(summary, quiz_count=5):
    prompt = f"""
다음 매장 매뉴얼 요약을 기반으로 객관식 퀴즈 {quiz_count}개를 생성해라.
반드시 JSON 배열만 반환해라.

JSON 형식:
[{{"question": "문제", "choices": ["보기1","보기2","보기3","보기4"], "answer": "정답", "explanation": "해설"}}]

요약 내용:
{summary}
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content