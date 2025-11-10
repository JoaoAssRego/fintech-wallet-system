from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Usa pydantic-settings para:
    - Carregar variáveis de ambiente
    - Validar tipos automaticamente
    - Fornecer valores padrão
    """
    
    # Application
    app_name: str = "Digital Wallet API"
    debug: bool = False
    
    # Database
    database_url: str
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuração do Pydantic 2.x
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Cria uma instância singleton de Settings.
    
    @lru_cache garante que Settings é criado apenas uma vez
    e reutilizado em toda aplicação (performance!).
    """
    return Settings()


# Instância global
settings = get_settings()