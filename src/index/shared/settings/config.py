from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(..., env="GEMINI_MODEL")
    model: str = Field(..., env="MODEL")
    mongo_uri: str = Field(..., env="MONGO_URI")

    class Config:
        env_file = ".env"

settings = Settings()
