from fastapi import APIRouter, Depends, HTTPException
import core.database as database
import core.contracts as contracts
import auth.deps as auth_deps
import chat.schemas as chat_schemas
import chat.repository as chat_repository
import chat.schemas as chat_schemas
import chat.context as chat_context
import llm.gateway.llm_service_client as llm_service_client
import chat.service as chat_service
import logging

logger = logging.getLogger("uvicorn.error")
 
router = APIRouter(
    prefix='/chat',
    tags=['chat'],
    dependencies=[Depends(auth_deps.token_not_blacklisted)]
)

@router.post('')
def chat_endpoint(
        request_data: chat_schemas.ChatRequest,
        db = Depends(database.get_db),
        current_user = Depends(auth_deps.get_current_user), 
        ):
    if(not chat_repository.get_conversations(db, request_data.conversation_id, current_user.id)):
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = chat_repository.create_message(
        db, 
        contracts.Role.user.value, 
        request_data.message, 
        request_data.conversation_id, 
        request_data.target_model)
    universal_context = chat_context.get_universal_context(db, request_data, current_user)
    completion = ''
    error = ''
    try:
        completion = llm_service_client.models_adapter(universal_context)
    except Exception as e:
        logger.error(f"LLM service call failed: {e}", exc_info=True)
        error = 'Ошибка отправки сообщения'
    new_message = chat_repository.create_message(
        db, 
        contracts.Role.assistant.value, 
        completion, 
        request_data.conversation_id, 
        universal_context.target_model,
        error
        )
    response = chat_service.pack_response(new_message)
    return response
    
    

@router.post('/conversations')
def crate_chat(
        request_data: chat_schemas.ConversationsRequest, 
        db = Depends(database.get_db), 
        current_user = Depends(auth_deps.get_current_user), 
):
    chat = chat_repository.create_conversations(db, request_data.title, current_user.id, request_data.default_model, request_data.system_prompt)
    return chat