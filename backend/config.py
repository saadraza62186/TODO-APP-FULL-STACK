from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 2
    DB_MAX_OVERFLOW: int = 5
    
    # Authentication
    BETTER_AUTH_SECRET: str
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Application
    DEBUG: bool = False
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
