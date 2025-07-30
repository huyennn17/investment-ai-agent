from index.api.models.client import ClientInput
from index.api.models.invest import AdviceOutput
from index.infra.llm import ChatGoogleGenerativeAIServices 
from langchain_core.language_models.chat_models import BaseChatModel


class InvestChainServices: 
    @property
    def _llm(self) -> BaseChatModel:
        return ChatGoogleGenerativeAIServices()._client
    
    def generate_investment_advice(self, client_input: ClientInput):

        prompt = f"""
    You are an expert financial advisor tasked with creating a personalized investment recommendation.

    Client Profile:
    - Name: {client_input.name}
    - Risk tolerance: {client_input.risk}
    - Sector preference: {client_input.sector}
    - Investment horizon: {client_input.investment_horizon}
    - Capital available: {client_input.capital_amount}
    - Income stability: {client_input.income_stability}
    - Experience level: {client_input.experience_level}
    - Country/Region: {client_input.location}

    Your goal:
    Suggest exactly two investment ideas that align with this profile.
    For each idea, include:
    1. What it is (name, type, example symbol if possible)
    2. Why it fits this client’s profile
    3. Key risks or considerations

    Assume the client wants practical, beginner-friendly advice. Keep it concise and free of jargon.
    Return your answer in structured format ONLY as defined in the tool schema.
 
    """

        model = self._llm.with_structured_output(AdviceOutput)
        return model.invoke(prompt)
