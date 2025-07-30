from index.api.models.budget import BudgetPlan
from index.infra.llm import ChatGoogleGenerativeAIServices
from langchain_core.language_models.chat_models import BaseChatModel


class BudgetChainServices:
    @property
    def _llm(self) -> BaseChatModel:
        return ChatGoogleGenerativeAIServices()._client

    def plan_budget(self, user_input: str) -> BudgetPlan:
        prompt = f"""
You are a professional **financial planning assistant** powered by a large language model. Your role is to create a **personalized monthly budget plan** for the user based on their natural-language description of income, lifestyle, goals, and expenses.

### OBJECTIVE ###
Return a response **strictly following** the `BudgetPlan` schema using the **50/30/20 budgeting rule** as a starting point.

### CORE RULES ###
- Default breakdown: **50% Needs**, **30% Wants**, **20% Savings**
- Adjust dynamically based on:
  - Debt burden
  - Financial goals (e.g., saving for a house, student loans)
  - Income level and stability
  - Cost of living (location, dependents, etc.)

### OUTPUT FORMAT ###
- Respond **only** with the structured data required by the `BudgetPlan` schema.
- Do **not** include natural language explanations, disclaimers, or headers.
- Values must be reasonable and internally consistent.

### EXAMPLES OF ADJUSTMENTS ###
- If user has significant debt: prioritize Savings and Needs, reduce Wants
- If user is financially stable with no debt: more flexibility for Wants
- If user has low income: ensure Needs are prioritized, reduce Savings but don’t remove

### USER INPUT ###
{user_input}

"""
        model = self._llm.with_structured_output(BudgetPlan)
        return model.invoke(prompt)
