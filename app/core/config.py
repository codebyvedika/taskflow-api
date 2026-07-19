from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskFlow API"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./dev.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()