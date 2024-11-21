from fastapi import UploadFile
from io import BytesIO
from pathlib import Path
import pandas as pd
import pdfplumber
from docx import Document
import json

ALLOWED_FILE_TYPES = [".csv", ".xlsx", ".xls", ".pdf", ".docx", ".json"]
MAX_FILE_SIZE = 5 * 1024 * 1024

async def process_file(file: UploadFile):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension == ".csv":
        return await extract_from_csv(file)
    elif file_extension in [".xlsx", ".xls"]:
        return await extract_from_excel(file)
    elif file_extension == ".pdf":
        return await extract_from_pdf(file)
    elif file_extension == ".docx":
        return await extract_from_docx(file)
    elif file_extension == ".json":
        return await extract_from_json(file)
    else:
        raise ValueError("Unsupported file type.")

# Helper Functions for Specific File Types
async def extract_from_csv(file):
    content = await file.read()
    try:
        df = pd.read_csv(BytesIO(content))
        return df.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

async def extract_from_excel(file):
    content = await file.read()
    try:
        df = pd.read_excel(BytesIO(content))
        return df.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

async def extract_from_pdf(file):
    content = await file.read()
    try:
        with pdfplumber.open(BytesIO(content)) as pdf:
            text = [page.extract_text() for page in pdf.pages]
        return {"content": text}
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")

async def extract_from_docx(file):
    content = await file.read()
    try:
        document = Document(BytesIO(content))
        text = [paragraph.text for paragraph in document.paragraphs]
        return {"content": text}
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {e}")

async def extract_from_json(file):
    content = await file.read()
    try:
        data = json.loads(content)
        return data
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")