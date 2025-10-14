import os
from openai import OpenAI

def get_client_for_model(model_name: str) -> OpenAI:
    if(model_name.startswith('deepseek')):
        base_url = "https://api.deepseek.com"
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=base_url)
    elif(model_name.startswith('gpt')):
        base_url = "https://api.openai.com/v1"
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), base_url=base_url)
    else:
        raise ValueError(f"Unknown model provider for '{model_name}'")
    return client