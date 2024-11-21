from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(main_router)