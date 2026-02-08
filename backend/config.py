from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"  # Default for testing
    DB_POOL_SIZE: int = 2
    DB_MAX_OVERFLOW: int = 5
    
    # Authentication
    BETTER_AUTH_SECRET: str = "default-secret-key-change-in-production-min-32-chars-long"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Application
    DEBUG: bool = False
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"
    
    # AI Service
    GOOGLE_API_KEY: str = ""
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra environment variables


settings = Settings()
