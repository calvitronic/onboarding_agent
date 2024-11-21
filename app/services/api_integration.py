from fastapi import HTTPException
import aiohttp
from retrying import retry
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Helper Function: Retryable API Call
@retry(wait_exponential_multiplier=1000, stop_max_attempt_number=3)
async def send_data_to_saas_api(data: list):
    SAAS_API_URL = os.getenv("MOCKOON_URL")  # Replace with the actual mock URL
    API_KEY = os.getenv("API_KEY")
    if not (API_KEY and SAAS_API_URL):
        raise ValueError("SAAS_API_URL or API_KEY is not set in the environment")
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(SAAS_API_URL, json=data, headers=headers) as response:
            if response.status != 200:
                error_message = await response.text()
                logger.error(f"API Error: {response.status} - {error_message}")
                raise HTTPException(status_code=502, detail="Error communicating with SaaS API.")
            return await response.json()