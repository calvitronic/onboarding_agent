from fastapi import APIRouter, UploadFile, HTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.extension import Limiter
from app.services.file_handler import process_file
from app.services.data_validator import validate_data
from app.services.transformer import transform_data

router = APIRouter()
limiter = Limiter(key_func=lambda x: "global")

@router.post("/upload", tags=["File Upload"])
@limiter.limit("5/minute")  # Limit to 5 requests per minute
async def upload_file(file: UploadFile):
    """
    Endpoint to upload and process a file.
    Supports CSV, Excel, PDF, DOCX, and JSON file types.
    """
    try:
        # Step 1: Extract data
        raw_data = await process_file(file)

        # Step 2: Validate data
        validated_data = await validate_data(raw_data)

        # Step 3: Transform data
        transformed_data = await transform_data(validated_data)

        return {"status": "success", "data": transformed_data}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Service is running"}

@router.get("/rate-limit-test", tags=["Test"])
@limiter.limit("1/second")  # Test endpoint with rate limiting
async def rate_limit_test():
    """
    Test endpoint to verify rate limiting is functional.
    """
    return {"status": "ok", "message": "Rate limiting is active"}