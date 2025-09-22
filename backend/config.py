from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    allowed_origins_raw: str = ""  # Raw string from .env

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]

    class Config:
        env_file = ".env"

settings = Settings()