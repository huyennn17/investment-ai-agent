from index.infra.llm import ChatGoogleGenerativeAIServices 
from langchain_core.language_models.chat_models import BaseChatModel

class GeneralChainServices:
    def _llm(self) -> BaseChatModel:
        return ChatGoogleGenerativeAIServices()._client

    def answer_general_question(self, question: str) -> str:
        prompt = (
            "You are a helpful and knowledgeable financial assistant. "
            "Answer the user's general finance question clearly and concisely:\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        llm = self._llm()
        return llm.invoke(prompt).content