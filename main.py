import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Nav-AI")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"

USER_PROFILE = """
The user's name is Abhinav Bhootra. He is a BCA final-year student in India.
He is learning Python, SQL, data analysis, AI and machine learning, and wants
to grow toward a Data Scientist role. He is a fresher and prefers practical,
beginner-friendly explanations. Use these details only when relevant.
Do not claim access to ChatGPT history, other apps, or files unless supplied.
""".strip()

MODE_INSTRUCTIONS = {
    "general": "Be helpful, accurate, natural, and conversational.",
    "learn": "Teach step by step in simple language with practical examples.",
    "code": "Help debug and explain code step by step. Avoid unnecessary rewrites.",
    "write": "Write naturally and clearly, avoiding robotic wording.",
    "brainstorm": "Offer creative options and practical next steps.",
}

class HistoryMessage(BaseModel):
    role: str
    text: str

class ChatMessage(BaseModel):
    message: str
    history: list[HistoryMessage] = Field(default_factory=list)
    mode: str = "general"

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME, "provider": "ollama-local"}

@app.post("/chat")
def chat(data: ChatMessage):
    user_message = data.message.strip()
    if not user_message:
        return {"reply": "Please enter a message."}

    system_prompt = (
        "You are Nav-AI, a friendly personal AI assistant.\n\n"
        f"USER PROFILE:\n{USER_PROFILE}\n\n"
        f"CURRENT MODE:\n{MODE_INSTRUCTIONS.get(data.mode, MODE_INSTRUCTIONS['general'])}\n\n"
        "Use the previous messages supplied in this request to keep context within this chat. "
        "If asked what you know about the user, summarize only the profile and facts actually present. "
        "Never pretend to remember a fact that is not available."
    )
    messages = [{"role": "system", "content": system_prompt}]
    for item in data.history[-12:]:
        role = "assistant" if item.role in ("assistant", "model") else "user"
        content = item.text.strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "messages": messages, "stream": False},
            timeout=180,
        )
        response.raise_for_status()
        reply = response.json().get("message", {}).get("content", "").strip()
        return {"reply": reply or "Sorry, I could not generate a response."}
    except requests.exceptions.ConnectionError:
        return {"reply": "Ollama is not running. Please open Ollama and try again."}
    except requests.exceptions.Timeout:
        return {"reply": "The local AI is taking too long. Please try again."}
    except requests.exceptions.RequestException as exc:
        print("OLLAMA ERROR:", repr(exc))
        return {"reply": "There was a problem connecting to local AI. Check the VS Code terminal."}
