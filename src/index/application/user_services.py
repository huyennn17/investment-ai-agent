from pymongo import ReturnDocument
from index.infra.db.mongo import db

class UserServices:
    async def create_new_user(self) -> str:
        result = await db.counters.find_one_and_update(
            {"_id": "user_id"},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return str(result["sequence_value"])
    