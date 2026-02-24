import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are an expert assistant.
Answer ONLY using the provided context.
If answer is not present, say you don't know.
"""


def generate_answer(query: str, context: str):

    full_prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}
"""

    response = model.generate_content(full_prompt)

    generated_text = response.text

    return {
        "answer": generated_text,
        "model": "gemini-1.5-flash"
    }
