from fastapi import FastAPI, Header, HTTPException
from openai import OpenAI
import os, logging
from .provider_factory import get_client_for_model
from dotenv import load_dotenv

load_dotenv('.env')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")


app = FastAPI(title="LLM Microservice", version="1.0")

INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/chat")
def chat_endpoint(body: dict, x_internal_token: str = Header(None)):
    if x_internal_token != INTERNAL_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid internal token")

    model = body.get("model")
    messages = body.get("messages")
    if not model or not messages:
        raise HTTPException(status_code=400, detail="Missing model or messages")

    try:
        client = get_client_for_model(model)
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )

        return completion.model_dump()
    except Exception as e:
        logger.exception(f"Provider error: {e}")
        raise HTTPException(status_code=502, detail="Provider upstream error")