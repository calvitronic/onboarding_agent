from fastapi import APIRouter, UploadFile, Request, HTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.extension import Limiter
from app.services.file_handler import process_file
from app.services.data_validator import validate_data
from app.services.transformer import transform_data
from app.services.api_integration import send_data_to_saas_api
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize the router and rate limiter
router = APIRouter()
limiter = Limiter(key_func=lambda x: "global")

@router.post("/upload", tags=["File Upload"])
@limiter.limit("5/minute", key_func=lambda request: request.client.host)  # Limit to 5 requests per minute
async def upload_file(request: Request, file: UploadFile):
    """
    Endpoint to upload and process a file.
    Supports CSV, Excel, PDF, DOCX, and JSON file types.
    """
    try:
        logger.debug("Received request to upload file.")
        
        # Step 1: Extract data
        logger.debug(f"Processing file: {file.filename}")
        raw_data = await process_file(file)
        logger.debug(f"Extracted raw data from {file.filename}: {raw_data}")
        
        # Step 2: Validate data (Commented out for now)
        # logger.debug("Validating data...")
        # validated_data = await validate_data(raw_data)
        # logger.debug(f"Validated data: {validated_data}")
        
        # Step 3: Transform data (Commented out for now)
        # logger.debug("Transforming data...")
        # transformed_data = await transform_data(validated_data)
        # logger.debug(f"Transformed data: {transformed_data}")
        
        # Send data to the mock SaaS API
        logger.debug("Sending data to SaaS API...")
        await send_data_to_saas_api(raw_data)
        logger.debug("Data successfully sent to SaaS API.")
        
        return {"status": "success", "data": raw_data}

    except Exception as e:
        # Log the error and return a user-friendly message
        logger.error(f"Error during file processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")

@router.get("/health", tags=["Health"])
async def health_check(request: Request):
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Service is running"}

@router.get("/rate-limit-test", tags=["Test"])
@limiter.limit("1/second", key_func=lambda request: request.client.host)  # Test endpoint with rate limiting
async def rate_limit_test(request: Request):
    """
    Test endpoint to verify rate limiting is functional.
    """
    return {"status": "ok", "message": "Rate limiting is active"}