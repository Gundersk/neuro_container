from openai import OpenAI
import core.contracts as contracts
import logging, os

logger = logging.getLogger(__name__)

def models_adapter(universal_context: contracts.UniversalChatRequest):
    if(universal_context.target_model.startswith('deepseek')):
        base_url = "https://api.deepseek.com"
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=base_url)
    elif(universal_context.target_model.startswith('gpt')):
        base_url = "https://api.openai.com/v1"
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), base_url=base_url)
    else:
        raise ValueError(f"Unknown model provider for '{universal_context.target_model}'")
    
    provider_message = list()
    provider_message.extend([m.model_dump() for m in universal_context.messages])
        
    if(universal_context.system_prompt):
        provider_message.insert(0, {'role': 'system', 'content': universal_context.system_prompt})
    try:
        completion = client.chat.completions.create(
            model=universal_context.target_model,
            messages=provider_message
        )
    except Exception as e:
        logger.error('Provider error: {type(e).__name__}, {e}', exc_info=True)
        raise

    return(completion.choices[0].message.content)