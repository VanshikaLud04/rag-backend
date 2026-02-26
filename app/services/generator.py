import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

system_prompt = """
You are a Retrieval Augmented assistant.

Rules:
- Answer ONLY from given context.
- Do not invent facts.
- If context is insufficient say: "Not found in document."
- Keep answer concise and factual.
- After answer, cite chunk IDs used.
"""


def stream_answer(query: str, context: str, sources: list):
    print("Streaming response")

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
        print("error", str(e))
        yield "\n[Generation failed]"