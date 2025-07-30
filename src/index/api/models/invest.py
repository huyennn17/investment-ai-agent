from pydantic import BaseModel, Field, HttpUrl, conint
from typing import List, Optional, Annotated

class InvestmentIdea(BaseModel):
    name: str = Field(..., description="Name of the investment or asset")
    type: str = Field(..., description="Type of investment (e.g., stock, ETF, bond)")
    symbol: Optional[str] = Field(None, description="Ticker or identifier if applicable (e.g., AAPL, SPY)")
    reason: str = Field(..., description="Why this idea fits the client’s profile")
    risk: str = Field(..., description="Main risks or cautions to consider")
    estimated_return: Optional[str] = Field(None, description="Expected return or growth potential")
    risk_score: Optional[Annotated[int, conint(ge=1, le=10)]] = Field(None, description="Risk level on a scale from 1 (low) to 10 (high)")
    confidence_level: Optional[str] = Field(None, description="LLM’s confidence in this recommendation (e.g. High, Medium)")
    more_info_link: Optional[HttpUrl] = Field(None, description="URL or source for learning more")

class AdviceOutput(BaseModel):
    ideas: List[InvestmentIdea] = Field(..., description="List of investment ideas tailored for the client")