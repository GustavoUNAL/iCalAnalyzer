from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # iCloud Credentials
    ICLOUD_USERNAME: str
    ICLOUD_APP_PASSWORD: str
    CALDAV_URL: str
    
    # API Settings
    API_VERSION: str
    DEBUG_MODE: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()