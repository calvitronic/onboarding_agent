from fastapi import APIRouter, UploadFile, Request, HTTPException
from slowapi.errors import RateLimitExceeded
from slowapi.extension import Limiter
from app.services.file_handler import process_file
from app.services.data_validator import analyze_and_fill_data
from app.services.api_integration import send_data_to_saas_api
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize the router and rate limiter
router = APIRouter()
limiter = Limiter(key_func=lambda x: "global")

# Define Validation Schema
validation_scheme = "class CustomerData(BaseModel): \
    customer_id: int = Field(..., gt=0, description=\"Unique customer ID\") \
    name: str = Field(..., min_length=1, max_length=100, description=\"Customer name\") \
    email: EmailStr = Field(..., description=\"Customer email address\") \
    signup_date: str = Field(..., pattern=r\"\d{4}-\d{2}-\d{2}\", description=\"Signup date in YYYY-MM-DD format\") \
    is_active: Optional[bool] = Field(default=True, description=\"Is the customer active\")"

@router.post("/upload", tags=["File Upload"])
@limiter.limit("5/minute", key_func=lambda request: request.client.host)  # Limit to 5 requests per minute
async def upload_file(request: Request, file: UploadFile):
    """
    Endpoint to upload and process a file.
    Supports CSV, Excel, PDF, DOCX, and JSON file types.
    """
    try:
        print("Received request to upload file.")
        
        # Step 1: Extract data
        print(f"Processing file: {file.filename}")
        raw_data = await process_file(file)
        print(f"Extracted raw data from {file.filename}: {raw_data}")
        
        #Step 2: Validate data
        print("Validating data...")
        validated_data = await analyze_and_fill_data(raw_data, validation_scheme)
        print(f"Validated data: {validated_data}")
        
        # Send data to the mock SaaS API
        print("Sending data to SaaS API...")
        await send_data_to_saas_api(validated_data)
        print("Data successfully sent to SaaS API.")
        
        return {
            "status": "success",
            "message": "File processed successfully.",
            "validated_data": validated_data,
        }
    except RateLimitExceeded as re:
        logger.error(f"Error during file processing: {re}", exc_info=True)
        raise HTTPException(status_code=429, detail="Too many requests: only 5 per minute allowed.")
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