from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "EdgeShield AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "edgeshield-secret-key-smart-hospital-iot-security-2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./edgeshield.db"
    
    # Ollama Local LLM Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_FALLBACK_MODEL: str = "phi3"
    LLM_TIMEOUT: int = 15  # seconds
    
    # ML Engine Settings
    MODEL_DIR: str = "./ml_pipeline/models"
    ANOMALY_THRESHOLD: float = -0.15
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
