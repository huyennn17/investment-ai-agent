from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from index.shared.settings.config import settings


class ChatGoogleGenerativeAIServices:
    @property 
    def _client(self) -> BaseChatModel: 
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            )
    
