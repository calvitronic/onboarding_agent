from app import app
import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 for local dev
    uvicorn.run(app, host="0.0.0.0", port=port)