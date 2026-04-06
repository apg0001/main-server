from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

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
    chatflow_api_key: str = Field(..., alias="CHATFLOW_API_KEY")

    # Workflow
    summary_workflow_api_key: str = Field(..., alias="SUMMARY_WORKFLOW_API_KEY")
    scoring_workflow_api_key: str = Field(..., alias="SCORING_WORKFLOW_API_KEY")

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