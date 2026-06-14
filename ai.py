from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(text):
    prompt = f"""
다음 매장 매뉴얼을 JSON 형식으로 요약해라. 반드시 JSON만 반환해라.

JSON 형식:
{{
  "summary": "전체 요약 1~2줄",
  "steps": ["절차1", "절차2"],
  "warnings": ["주의사항1"]
}}

매뉴얼 내용:
{text}
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content