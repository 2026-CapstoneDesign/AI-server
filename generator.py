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
        model="gpt-4o-mini",
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
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content

# generator.py 맨 아래에 추가할 코드

def generate_recommendations(summary):
    prompt = f"""
다음 매장 매뉴얼 요약을 기반으로, 새로 온 알바생들이 매장에 출근해서 가장 궁금해하고 자주 물어볼 법한 '핵심 추천 질문 8개'를 생성해라.

조건:
- 반드시 순수한 JSON 문자열 배열(List)만 반환해라. (부연설명이나 마크다운 따옴표 포함 절대 금지)
- 질문은 알바생이 매장에서 겪을 상황에 맞게 아주 구체적이고 간결한 의문문 문장으로 생성해라.
- 상황과 맥락에 맞게 가장 자연스러운 한국어 어미(~하나요?, ~무엇인가요?, ~일은?)를 골라서 사용해라.

적절한 예시:
- "출근 시 가장 먼저 해야 할 일은?"
- "시재가 맞지 않을 경우 어떻게 해야 하나요?"
- "상품권은 어디에서 확인하고 입력해야 하나요?"

JSON 형식:
[
  "질문 내용 1",
  "질문 내용 2",
  "질문 내용 3",
  "질문 내용 4",
  "질문 내용 5",
  "질문 내용 6",
  "질문 내용 7",
  "질문 내용 8"
]

요약 내용:
{summary}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini", # ⚠️ 작성하신 스펠링 오타(4.1-mini)가 에러를 낼 수 있어서 안정적인 공식 명칭으로 정돈했습니다.
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content