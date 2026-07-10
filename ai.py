from dotenv import load_dotenv
import os

load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(text):
    prompt = f"""
    다음 매뉴얼을 요약해라.

    JSON 형식:
    {{
      "summary": "",
      "steps": [],
      "warnings": []
    }}

    텍스트:
    {text}
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def ask_chatbot(question, manual_text):
    prompt = f"""
너는 매장의 친절하지만 아주 명쾌하고 깔끔한 베테랑 매니저야.
제공된 [매뉴얼 원문]을 바탕으로 [알바생의 질문]에 대해 답변을 생성해라.

조건:
- 절대 매뉴얼 원문을 통째로 길게 복사해서 대답하지 마라.
- 알바생이 바쁜 근무 중에 빠르게 읽을 수 있도록, 딱 필요한 핵심 정답만 '1~2줄 내외'로 극도로 간결하게 요약해서 답변해라.
- 문장 끝은 "~한다.", "~해야 합니다.", "~하면 됩니다." 처럼 명확하고 깔끔하게 맺어라.

좋은 예시:
- "동전통 아래 보관된 곳에서 상품권을 확인한 후 입력하시면 됩니다."
- "유니폼으로 환복 후 포스기 인수인계 버튼을 가장 먼저 눌러야 합니다."

[매뉴얼 원문]:
{manual_text}

[알바생의 질문]:
{question}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content