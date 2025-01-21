from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

class DashboardSettings(BaseSettings):
    # API Settings
    API_BASE_URL: str
    
    # Dashboard Settings
    DASH_HOST: str = "localhost"
    DASH_PORT: int = 8050
    DASH_DEBUG: bool = True
    DASH_TITLE: str = "Calendar Analytics Dashboard"
    
    # Theme Settings
    THEME_BOOTSTRAP: str = "BOOTSTRAP"
    PRIMARY_COLOR: str = "#007bff"
    SECONDARY_COLOR: str = "#6c757d"
    
    # Cache Settings
    CACHE_TIMEOUT: int = 300
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env.dashboard"
        case_sensitive = True

@lru_cache()
def get_settings():
    return DashboardSettings()

def setup_logging(settings: DashboardSettings = None):
    if settings is None:
        settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT
    )