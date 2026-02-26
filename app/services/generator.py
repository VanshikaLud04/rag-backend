import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

system_prompt = """
You are a Retrieval Augmented assistant.

Rules:
- Answer ONLY from given context.
- Do not invent facts.
- If context is insufficient say: "Not found in document."
- Keep answer concise and factual.
- After answer, cite chunk IDs used.
"""


def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Google API key not found. "
            "Set GOOGLE_API_KEY in environment."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )


def stream_answer(query: str, context: str, sources: list):
    print("Streaming response")

    llm = get_llm()   

    source_text = ",".join(map(str, sources))

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"""
Sources:
{source_text}

Context:
{context}

Question:
{query}
"""
        )
    ]

    try:
        for chunk in llm.stream(messages):
            if chunk.content:
                yield chunk.content

    except Exception as e:
        print("error:", str(e))
        yield "\n[Generation failed]"