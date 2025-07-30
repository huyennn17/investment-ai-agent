from fastapi import APIRouter
from index.application.chat_services import ChatServices

router = APIRouter(prefix="/chat", tags=["Chat"])
chat_service = ChatServices()

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    return await chat_service.get_chat_history(user_id)
