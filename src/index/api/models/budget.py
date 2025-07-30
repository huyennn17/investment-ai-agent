from pydantic import BaseModel, Field
from typing import Optional

class BudgetPlan(BaseModel):
    essentials: float
    wants: float
    savings: float
    suggested_improvement: Optional[str]
