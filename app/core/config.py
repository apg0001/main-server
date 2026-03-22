from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    port: int = Field(default=8001, alias="PORT")
    app_name: str = "News Monitoring API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True
    refresh_token_expire_days: int = 14

    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()