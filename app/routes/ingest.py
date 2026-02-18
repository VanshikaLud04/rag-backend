from fastapi import APIRouter, File, UploadFile
import os, uuid

router= APIRouter()
UPLOAD_DIR = "data/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()

    with open(path, "wb") as f:
        f.write(content)

    return {"saved_as": filename}





