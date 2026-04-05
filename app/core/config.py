from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # 기본 앱 설정
    # =========================
    app_name: str = "News Monitoring API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # =========================
    # 인증 / DB
    # =========================
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 14

    # =========================
    # Dify (AI)
    # =========================
    dify_base_url: str
    dify_api_key: str
    dify_request_timeout: int = 30

    # =========================
    # TransNews (크롤링 서버) 
    # =========================
    transnews_base_url: str
    transnews_request_timeout: int = 20

    # =========================
    # ENV 설정
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()