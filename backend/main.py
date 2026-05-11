from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from pdfminer.high_level import extract_text
import shutil
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Text Summarizer API is running"}

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    framework="pt"
)

# Summarize text
@app.post("/summarize-text/")
async def summarize_text(text: str = Form(...)):
    summary = summarizer(text, max_length=300, min_length=30, do_sample=False)
    return {"summary": summary[0]["summary_text"]}

# Summarize PDF
@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    extracted_text = extract_text(file_path)

    os.remove(file_path)

    if not extracted_text.strip():
        return {"summary": "No readable text found in PDF"}

    summary = summarizer(extracted_text[:2000], max_length=130, min_length=30, do_sample=False)

    return {"summary": summary[0]["summary_text"]}