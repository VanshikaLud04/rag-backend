from pypdf import PdfReader

def extract_text(file_path : str) -> str :
    text= ""
    if file_path.endswith(".txt") :
        with open (file_path, "r", encoding="utf-8") as f:
            text=f.read()
    
    elif file_path.endswith(".pdf") :
        reader= PdfReader(file_path)
        for page in reader.pages :
            page_text= page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text
