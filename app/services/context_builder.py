def build_context(chunks):
    return "\n\n".join([c["text"] for c in chunks]) 