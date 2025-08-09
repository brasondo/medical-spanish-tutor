from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
from .ui import router as ui_router


load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "Medical Spanish Tutor"))
app.include_router(ui_router) 

# Load persona/system prompt
with open("prompts/medspan_roleplay.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().strip()

# Hugging Face (free hosted) settings
HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # required
HF_TEXT_MODEL = os.getenv("HF_TEXT_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

if not HF_API_TOKEN:
    raise RuntimeError("Missing HF_API_TOKEN in your .env file.")

client = InferenceClient(model=HF_TEXT_MODEL, token=HF_API_TOKEN)

class ChatMessage(BaseModel):
    user: str
    scenario: str | None = None
    level: str | None = "A2"

@app.get("/health")
def health():
    return {"ok": True, "model": HF_TEXT_MODEL}

def build_messages(system: str, user: str, scenario: str | None, level: str | None):
    sceneline = f"Escenario: {scenario or 'general'}"
    levelline = f"Nivel: {level or 'A2'}"
    sys = (
        "Eres Clara, una tutora de Español médico. Guía con empatía, "
        "corrige suavemente, evita consejos médicos reales y usa usted por defecto.\n\n"
        + system
    )
    usr = f"{sceneline} | {levelline}\n{user}"
    return [
        {"role": "system", "content": sys},
        {"role": "user", "content": usr},
    ]

@app.post("/chat")
def chat(msg: ChatMessage):
    messages = build_messages(SYSTEM_PROMPT, msg.user, msg.scenario, msg.level)
    try:
        resp = client.chat_completion(
            messages=messages,
            max_tokens=240,      # tokens to generate
            temperature=0.8,     # creativity
            top_p=0.95           # nucleus sampling
            # NOTE: no repetition_penalty here (unsupported)
        )
        # Robustly extract content (HF returns OpenAI-like shape)
        choice = resp.choices[0]
        # some clients expose .message as dict, others as object
        message = getattr(choice, "message", None) or choice.get("message", {})
        content = getattr(message, "content", None) or message.get("content", "") or ""
        reply = content.strip()

        if not reply or reply == "...":
            reply = "Entiendo. Empecemos con algo sencillo: ¿dónde le duele exactamente y desde cuándo?"

        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Hugging Face inference error: {e}")