import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# -----------------------------------
# OPENAI CLIENT
# -----------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -----------------------------------
# GENERATE ANSWER
# -----------------------------------

def generate_answer(question, context):

    prompt = f"""

You are a healthcare data assistant.

IMPORTANT RULES:
- Use ONLY provided context
- Do NOT invent values
- Do NOT provide diagnosis
- Do NOT provide treatment advice
- Keep answer factual and concise

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    answer = response.choices[0].message.content

    return answer


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    question = "Summarize CRP history"

    context = """
    Latest CRP value: 3.64
    Trend: fluctuating

    CRP history:
    2024-04-10: 6.5 mg/L
    2025-02-08: 1.67 mg/L
    2025-05-19: 10.07 mg/L
    2025-09-24: 3.64 mg/L

    Overall pattern: fluctuating.
    """

    answer = generate_answer(
        question,
        context
    )

    print("\n--- ANSWER ---\n")

    print(answer)