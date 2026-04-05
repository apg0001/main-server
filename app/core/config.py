from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "News Monitoring API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    refresh_token_expire_days: int = 14
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Chatflow
    dify_base_url: str
    chatflow_api_key: str

    # Workflow
    summary_workflow_api_key: str
    scoring_workflow_api_key: str

    # Knowledge
    knowledge_api_key: str
    dify_dataset_id: str
    dify_article_id_metadata_field_id: str

    dify_request_timeout: int = 30
    transnews_base_url: str
    transnews_request_timeout: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()