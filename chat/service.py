import core.contracts as contracts
import chat.schemas as chat_schemas
import chat.models as chat_models

def pack_response(message: chat_models.Messages) -> chat_schemas.ChatResponse:
    chat_message = contracts.ChatMessage(role=contracts.Role.assistant.value, content=message.content)
    chat_response = chat_schemas.ChatResponse(conversation_id=message.conversation_id, message=chat_message, model=message.model)
    return chat_response



