from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Matrix chatbot backend is running"}

@app.post("/chat")
async def chat(payload: dict):
    user_message = payload.get("message")

    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content": user_message}],
                "temperature": 0.7
            },
            timeout=30
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq error: {response.text}")

        data = response.json()

        reply = data["choices"][0]["message"]["content"]

        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
