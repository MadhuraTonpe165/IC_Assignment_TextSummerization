from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class StoryRequest(BaseModel):
    story: str
    max_output_tokens: int = 500

@app.post("/summarize")
def generate_story(request: StoryRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    # Prompt to instruct translation
    prompt = (
        f"summarise the following text in a clerly and precisely to maximum {request.max_output_tokens} tokens:\n\n"
        f"{request.story}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)


    

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    story_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return {"story": story_text}
