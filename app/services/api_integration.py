import aiohttp
from retrying import retry
import os
from dotenv import load_dotenv

load_dotenv()

# Helper Function: Retryable API Call
@retry(wait_exponential_multiplier=1000, stop_max_attempt_number=3)
async def send_data_to_saas_api(data):
    POSTMAN_KEY = os.getenv("POSTMAN_KEY")
    POSTMAN_URL = os.getenv("POSTMAN_URL")  # Replace with the actual mock URL
    if not (POSTMAN_KEY and POSTMAN_URL):
        raise ValueError("POSTMAN_URL and/or POSTMAN_KEY not set in the environment.")
    
    payload = {"CustomerData": data}  # Replace with your payload
    headers = {
        "Content-Type": "application/json",  # Specify JSON content type
        "x-api-key": POSTMAN_KEY  # Add the API key to the headers
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{POSTMAN_URL}/upload", json=payload, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                print("Success:", response_data)
            else:
                error_message = await response.text()
                print(f"Error: {response.status} - {error_message}")