from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from .routes import router as main_router

# Create FastAPI app
app = FastAPI(
    title="AI Customer Onboarding Agent",
    description="An API to process file uploads and interact with a SaaS API.",
    version="1.0.0"
)

# Add rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add process time in the response headers.
    Measures the time taken to process the request and adds it to the response header.
    """
    start_time = time.time()
    response = await call_next(request)
    
    # Only try to measure elapsed time if the response is not streaming
    if isinstance(response, Response):
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
    
    return response

app.include_router(main_router)