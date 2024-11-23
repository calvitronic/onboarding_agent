import aiohttp
from retrying import retry
import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Load the appropriate .env file
if ENVIRONMENT == 'production':
    load_dotenv('.env.prod')
else:
    load_dotenv('.env.dev')

# Helper Function: Retryable API Call
@retry(wait_exponential_multiplier=1000, stop_max_attempt_number=3)
async def send_data_to_saas_api(data: list):
    POSTMAN_KEY = os.getenv("POSTMAN_KEY")
    POSTMAN_URL = os.getenv("POSTMAN_URL")  # Replace with the actual mock URL
    if not (POSTMAN_KEY and POSTMAN_URL):
        raise ValueError("SAAS_API_URL or API_KEY is not set in the environment")
    
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