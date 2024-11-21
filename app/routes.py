from fastapi import APIRouter, UploadFile, Request, HTTPException
from fastapi.templating import Jinja2Templates
from slowapi.errors import RateLimitExceeded
from slowapi.extension import Limiter
from app.services.file_handler import process_file
from app.services.data_validator import validate_data
from app.services.transformer import transform_data
from app.services.api_integration import send_data_to_saas_api

# Initialize Jinja2 template renderer
templates = Jinja2Templates(directory="../templates")

# Initialize the router and rate limiter
router = APIRouter()
limiter = Limiter(key_func=lambda x: "global")

@router.post("/upload", tags=["File Upload"])
@limiter.limit("5/minute")  # Limit to 5 requests per minute
async def upload_file(request: Request, file: UploadFile):
    """
    Endpoint to upload and process a file.
    Supports CSV, Excel, PDF, DOCX, and JSON file types.
    """
    try:
        # Step 1: Extract data
        raw_data = await process_file(file)

        # Step 2: Validate data
        # validated_data = await validate_data(raw_data)

        # Step 3: Transform data
        # transformed_data = await transform_data(validatsed_data)

        await send_data_to_saas_api(raw_data)

        return {"status": "success", "data": raw_data}

    except RateLimitExceeded as re:
        # Handle rate limiting error
        raise HTTPException(status_code=429, detail="Limited to 5 requests per minute")
    except ValueError as ve:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # General error handler
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/health", tags=["Health"])
async def health_check(request: Request):
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Service is running"}

@router.get("/rate-limit-test", tags=["Test"])
@limiter.limit("1/second")  # Test endpoint with rate limiting
async def rate_limit_test(request: Request):
    """
    Test endpoint to verify rate limiting is functional.
    """
    return {"status": "ok", "message": "Rate limiting is active"}