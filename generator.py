from openai import OpenAI
client = OpenAI()

def generate_content(summary):
    prompt = f"""
    다음 내용을 카드형 학습 콘텐츠로 만들어라.

    {summary}

    JSON 배열:
    [
      {{ "title": "", "content": "" }}
    ]
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def generate_quiz(summary):
    prompt = f"""
    다음 내용을 기반으로 객관식 퀴즈 5개 생성

    {summary}

    JSON:
    [
      {{
        "question": "",
        "choices": ["", "", ""],
        "answer": ""
      }}
    ]
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content