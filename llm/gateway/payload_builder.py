from core.contracts import UniversalChatRequest
from openai import OpenAI
import os

def build_openai_payload(universal_context: UniversalChatRequest):
    
    payload = list()
    payload.extend([m.model_dump() for m in universal_context.messages])
        
    if(universal_context.system_prompt):
        payload.insert(0, {'role': 'system', 'content': universal_context.system_prompt})

    return {
        "messages": payload,
        "model": universal_context.target_model
    }