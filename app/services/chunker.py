def chunk_text(text: str, size: int=500,overlap :int=50):
    words=text.split()
    chunks=[]
    start=0

    step=size- overlap

    while start<len(words):
        parts= words[start: start+size]
        chunk="".join(parts)
        chunks.append(chunk)
        start+=step

        return chunks

