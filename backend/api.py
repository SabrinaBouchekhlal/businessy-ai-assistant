import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()

from agent import agent  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="Businessy AI Assistant", version="0.1.0")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list, max_length=30)

class ChatResponse(BaseModel):
    reply: str
    demo: bool = True

def message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                pieces.append(block.get("text", ""))
            elif isinstance(block, str):
                pieces.append(block)
        return "\n".join(pieces).strip()
    return str(content)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Businessy AI Assistant", "data": "fictional demo data"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is missing. Add GOOGLE_API_KEY to backend/.env and restart the server."
        )
    messages = []
    for item in body.history:
        role = item.get("role")
        content = item.get("content", "")
        if role in {"user", "assistant"} and content.strip():
            messages.append({"role": role, "content": content[:4000]})
    messages.append({"role": "user", "content": body.message})
    try:
        result = agent.invoke({"messages": messages})
        reply = message_text(result["messages"][-1].content)
        return ChatResponse(reply=reply)
    except Exception as exc:
        # Avoid exposing secrets, request headers, or internal tracebacks to the browser.
        print(f"Businessy agent error: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=502, detail="The assistant could not complete that request. Check the server terminal and Gemini API configuration.")

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")
