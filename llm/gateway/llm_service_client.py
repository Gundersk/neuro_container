import httpx, os, logging
from .payload_builder import build_openai_payload
import core.contracts as contracts

logger = logging.getLogger(__name__)
from dotenv import load_dotenv

load_dotenv('.env')


LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://127.0.0.1:8010/v1/chat")
INTERNAL_TOKEN = os.getenv("INTERNAL_TOKEN")

def models_adapter(ctx: contracts.UniversalChatRequest):
    payload = build_openai_payload(ctx)
    try:
        response = httpx.post(
            LLM_SERVICE_URL,
            json=payload,
            headers={'X-Internal-Token': INTERNAL_TOKEN},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f'LLM service error: {e}', exc_info=True)
        raise