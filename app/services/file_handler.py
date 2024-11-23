from fastapi import UploadFile
from io import BytesIO
from pathlib import Path
import pandas as pd
import pdfplumber
from docx import Document
import json
import os

base_directory = os.getcwd()
ALLOWED_FILE_TYPES = ["csv", "xlsx", "xls", "pdf", "docx", "json"]
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024 # 10 MB

async def process_file(file: UploadFile):
    
    file_extension = Path(file.filename).suffix.lower()[1:]
    if file_extension not in ALLOWED_FILE_TYPES:
        raise ValueError("Unsupported file type.")
    if file.size > MAX_FILE_SIZE_BYTES:
        raise ValueError("File size exceeds 10MB.")
    if not is_safe_file_upload(Path(file.filename), base_directory):
        raise ValueError("Potential directory traversal attack.")
    
    if file_extension == "csv":
        return await extract_from_csv(file)
    elif file_extension in ["xlsx", "xls"]:
        return await extract_from_excel(file)
    elif file_extension == "pdf":
        return await extract_from_pdf(file)
    elif file_extension == "docx":
        return await extract_from_docx(file)
    elif file_extension == "json":
        return await extract_from_json(file)
    
def is_safe_file_upload(upload_path: str, upload_directory: str) -> bool:
    """
    Check if the uploaded file path is within the intended upload directory.

    Args:
        upload_path (str): The path of the uploaded file (user input).
        upload_directory (str): The base directory for uploads.

    Returns:
        bool: True if the upload is safe, False otherwise.
    """
    # Convert paths to Path objects
    upload_path = Path(upload_path)
    upload_directory = Path(upload_directory).resolve()

    # Resolve the absolute path of the upload
    resolved_path = (upload_directory / upload_path).resolve()

    # Check if the resolved path is within the upload directory
    return resolved_path.is_file() or upload_directory in resolved_path.parents

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
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")

async def extract_from_docx(file):
    content = await file.read()
    try:
        document = Document(BytesIO(content))
        text = [paragraph.text for paragraph in document.paragraphs]
        return text
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {e}")

async def extract_from_json(file):
    content = await file.read()
    try:
        data = json.loads(content)
        return data
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")