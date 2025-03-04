from pydantic_settings import BaseSettings

class Settings(BaseSettings):  
    CONFIDENCE_THRESHOLD: float = 0.5

settings = Settings()