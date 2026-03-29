import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

system_prompt = """
You are a Retrieval Augmented Generation assistant.

Rules:
- Answer ONLY from the given context.
- Do not invent or assume facts not present in the context.
- If context is insufficient, say exactly: "Not found in document."
- Keep answers concise and factual.
- After your answer, cite the chunk IDs used.
"""


def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY not set. Add it to your .env file."
        )
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=api_key
    )


def stream_answer(query: str, context: str, sources: list):
    """
    Args:
        query:   the user's question
        context: retrieved document chunks joined as a string
        sources: list of chunk IDs used
    Yields:
        str chunks of the streaming response
    """
    print("Streaming response...")
    llm = get_llm()

    source_text = ", ".join(map(str, sources))

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""Sources: {source_text}

Context:
{context}

Question: {query}
""")
    ]

    try:
        for chunk in llm.stream(messages):
            if chunk.content:
                yield chunk.content
    except Exception as e:
        print(f"Generation error: {e}")
        yield "\n[Generation failed. Check your GOOGLE_API_KEY.]"