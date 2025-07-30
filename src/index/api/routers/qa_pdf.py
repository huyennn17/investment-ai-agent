from fastapi import APIRouter, UploadFile, File, Form, Request, Response, HTTPException
from index.api.models.pdf import PDFAnswer
from index.application.pdf_chain import PDFChainServices
from index.application.chat_services import ChatServices
from index.application.user_services import UserServices

router = APIRouter(prefix="/pdf", tags=["PDF QA"])

pdf_chain = PDFChainServices()
chat_logger = ChatServices()
user_services = UserServices()

@router.post("/", response_model=PDFAnswer)
async def qa_over_pdf(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    question: str = Form(...)
):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    content = await file.read()
    result = pdf_chain.answer_from_pdf(content, question)

    await chat_logger.save_chat(
        user_id=user_id,
        message=question,
        response=result.model_dump_json(),
        source="qa_pdf"
    )

    return result
