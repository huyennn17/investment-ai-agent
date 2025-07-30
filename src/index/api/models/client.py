from pydantic import BaseModel, Field

class ClientInput(BaseModel):
    name: str  = Field(default="client")
    risk: str              # "low", "medium", "high"
    sector: str            # e.g. "tech", "healthcare"
    investment_horizon: str  # "short-term", "long-term"
    capital_amount: float  # e.g. 5000.0
    income_stability: str  # "stable", "fluctuating"
    experience_level: str  # "beginner", "intermediate", "expert"
    location: str          # optional, for market region (e.g. "US", "Asia")
    
