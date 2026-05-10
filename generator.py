from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_content(summary):
    prompt = f"""
다음 내용을 알바생이 보기 쉬운 카드형 학습 콘텐츠로 만들어라.

조건:
- 반드시 JSON 배열만 반환해라.
- 각 항목은 title, content를 가진다.
- 설명은 짧고 이해하기 쉽게 작성해라.

JSON 형식:
[
  {{
    "title": "제목",
    "content": "내용"
  }}
]

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
다음 매장 매뉴얼 요약을 기반으로 알바생 교육용 객관식 퀴즈 {quiz_count}개를 생성해라.

조건:
- 반드시 JSON 배열만 반환해라.
- 각 문제는 question, choices, answer, explanation을 가진다.
- choices는 보기 4개로 구성한다.
- answer는 choices 중 정답 문자열 그대로 작성한다.
- explanation은 왜 정답인지 짧게 작성한다.

JSON 형식:
[
  {{
    "question": "문제 내용",
    "choices": ["보기1", "보기2", "보기3", "보기4"],
    "answer": "정답 보기",
    "explanation": "해설"
  }}
]

요약 내용:
{summary}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content