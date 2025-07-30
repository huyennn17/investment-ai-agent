from fastapi import APIRouter
from index.application.user_services import UserServices

router = APIRouter(prefix="/user", tags=["User"])

user_services = UserServices()

@router.get("/get_id")
async def get_id():
    user_id = await user_services.create_new_user()
    return {"user_id": user_id}