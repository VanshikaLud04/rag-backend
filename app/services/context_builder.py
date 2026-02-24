def build_context(chunks):

    context= "\n\n".join([c["text"] for c in chunks]) 
    
    return context