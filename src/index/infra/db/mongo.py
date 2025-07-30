from motor.motor_asyncio import AsyncIOMotorClient
from index.shared.settings.config import settings

MONGO_URI = settings.mongo_uri
mongo_client = AsyncIOMotorClient(MONGO_URI)

db = mongo_client["investmentai"]