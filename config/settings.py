from pydantic import BaseSettings, Field
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = Field(default="sqlite:///data/agri.db", env="DATABASE_URL")
    
    # API Configuration
    api_title: str = "Smart Agriculture API"
    api_version: str = "1.0.0"
    allowed_origins: List[str] = Field(default=["http://localhost:8501"], env="ALLOWED_ORIGINS")
    
    # Security
    api_key_header: str = "X-API-Key"
    api_keys: List[str] = Field(default=[], env="API_KEYS")  # Load from env
    
    # Agricultural Thresholds
    soil_moisture_critical: float = 20.0
    soil_moisture_low: float = 40.0
    soil_moisture_optimal_min: float = 60.0
    soil_moisture_optimal_max: float = 80.0
    soil_moisture_excess: float = 85.0
    
    temp_optimal_min: float = 15.0
    temp_optimal_max: float = 30.0
    temp_high: float = 30.0
    temp_extreme: float = 35.0
    
    humidity_low: float = 40.0
    
    # Plot Configuration
    default_plot_area_m2: float = 100.0
    root_depth_m: float = 0.3
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/agri_system.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
