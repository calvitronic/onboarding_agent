from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
  organization='org-El5mKTVBrUsQwWsmK2v1V7t8',
  project='proj_HEG9R3MNHvaBJoNSPzh4dwvx',
  api_key=os.getenv("OPENAI_KEY")
)

# Validation Function
async def analyze_and_fill_data(data, schema):
    prompt = f"""
    Given the following schema: {schema},
    Analyze the record: {data},
    Fill in missing values of the schema using the above record as necessary.
    Output ONLY the completed record (with any missing values set to null) in JSON_string format.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a data analyzer."},
                    {"role": "user", "content": prompt}],
        )
    except ValueError as ve:
        print(f"Error: {ve}")

    return response.choices[0].message.content