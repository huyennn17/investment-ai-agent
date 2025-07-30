from .gemini import ChatGoogleGenerativeAIServices
from index.shared.settings.config import Settings
from langchain_core.language_models.chat_models import BaseChatModel

class ChatLLMServices: 
    def __init__(self, settings: Settings): 
        self.model_name = settings.model
    
    @property
    def _google_client(self): 
        return ChatGoogleGenerativeAIServices._client
    
    @property
    def _llm(self) -> BaseChatModel: 
        if self.name_model == "google": 
            return self._google_client
        else: 
            return "error"
        
# settings = Settings()
# llm_services = ChatLLMServices(settings=settings)