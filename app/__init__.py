from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
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
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(response.elapsed.total_seconds())
    return response

# Include routes
app.include_router(main_router)

__all__ = ["app"]