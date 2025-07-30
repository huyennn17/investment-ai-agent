from fastapi import APIRouter, Body, HTTPException, Request, Response
from index.api.models.budget import BudgetPlan
from index.application.budget_chain import BudgetChainServices
from index.application.chat_services import ChatServices
from index.application.user_services import UserServices

router = APIRouter(prefix="/budget", tags=["Budgeting"])

budget_chain = BudgetChainServices()
chat_logger = ChatServices()
user_services = UserServices()


@router.post("/", response_model=BudgetPlan)
async def get_budget_plan(
    request: Request,
    response: Response,
    user_input: str = Body(..., embed=True)
):
    user_id = request.query_params.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    result = budget_chain.plan_budget(user_input)

    await chat_logger.save_chat(
        user_id=user_id,
        message=user_input,
        response=result.model_dump_json(),
        source="budget"
    )

    return result
