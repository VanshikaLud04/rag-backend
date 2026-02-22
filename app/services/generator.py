def generate_answer(query, context):

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{query}

Answer 
"""

    # placeholder response
    return f"Generated answer using context of length {len(context)}"