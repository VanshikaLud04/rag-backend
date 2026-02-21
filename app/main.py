from fastapi import FastAPI, File, UploadFile, Form , APIRouter
from fastapi.responses import JSONResponse
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import shutil
from app.routes import health, ingest

app= FastAPI(title= "RAG Backend")

app.include_router(health.router)
app.include_router(ingest.router)

