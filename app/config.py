from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # Application
    app_name: str = "Digital Wallet API"
    debug: bool = False

    # Database
    database_url: str

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:

    return Settings()

# Instância global
settings = get_settings()
