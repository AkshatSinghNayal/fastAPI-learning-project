from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore") 
    DATABASE_URL: str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME : int 
    EMAIL_USER : str
    EMAIL_PASSWORD : str

settings = Settings()