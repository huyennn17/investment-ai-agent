from fastapi import APIRouter, Request, Response, HTTPException
from index.api.models.client import ClientInput
from index.api.models.invest import AdviceOutput
from index.application.invest_chain import InvestChainServices
from index.application.chat_services import ChatServices
from index.application.user_services import UserServices

router = APIRouter(prefix="/invest", tags=["Investment"])

invest_chain = InvestChainServices()
chat_logger = ChatServices()
user_services = UserServices()

@router.post("/", response_model=AdviceOutput)
async def get_investment_advice(
    request: Request,
    response: Response,
    client_input: ClientInput
):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # 2. Generate investment advice from LLM
    result = invest_chain.generate_investment_advice(client_input)

    # 3. Log to MongoDB
    await chat_logger.save_chat(
        user_id=user_id,
        message=client_input.model_dump_json(),
        response=result.model_dump_json(),
        source="invest"
    )

    # 4. Return response
    return result
