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
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content