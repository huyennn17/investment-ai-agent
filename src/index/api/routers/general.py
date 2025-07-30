from fastapi import APIRouter, Body, Request, Response, HTTPException
from index.application.general_chain import GeneralChainServices
from index.application.chat_services import ChatServices
from index.application.user_services import UserServices

router = APIRouter(prefix="/general", tags=["General Finance"])

general_chain = GeneralChainServices()
chat_logger = ChatServices()
user_services = UserServices()

@router.post("/")
async def handle_general_question(
    request: Request,
    response: Response,
    user_input: str = Body(..., embed=True)
):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    answer = general_chain.answer_general_question(user_input)

    await chat_logger.save_chat(
        user_id=user_id,
        message=user_input,
        response=answer,
        source="general"
    )

    return {"answer": answer}
