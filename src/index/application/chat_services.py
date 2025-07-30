from index.infra.db.mongo import db
from datetime import datetime, timezone
import json


class ChatServices:
    def __init__(self):
        self.collection = db.chat_history

    async def save_chat(self, user_id: str, message: str, response: str, source: str = "unknown"):
        await self.collection.insert_one({
            "user_id": user_id,
            "message": message,
            "response": response,
            "source": source,  # e.g., 'budget', 'invest', 'pdf'
            "timestamp": datetime.now(timezone.utc)
        })

    async def get_chat_history(self, user_id: str, limit: int = 100):
        cursor = self.collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        chats = await cursor.to_list(length=limit)

        for chat in chats:
            chat["_id"] = str(chat["_id"])  # convert ObjectId to string
            if isinstance(chat["response"], str):
                try:
                    chat["response"] = json.loads(chat["response"])
                except json.JSONDecodeError:
                    pass  # keep as-is if not valid JSON string

        return chats


