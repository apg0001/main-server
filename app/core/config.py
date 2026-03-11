from pydantic_settings import BaseSettings, SettingsConfigDict

#BaseSetting은 환경변수(env)와 설정값을 관리하는 클래스
class Settings(BaseSettings):
    app_name: str = "News Monitoring API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True #개발 모드 - 로그 많이 출력, 오류메시지 자세히 표시
    
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/news_monitoring"
    
    #JWT 설정들
    secret_key: str = "-"
    algorithm: str = "HS256" #JWT 암호화 방식(가장 많이 쓰이는 방식으로 일단)
    access_token_expire_minutes: int = 60
    
    #환경변수 설정
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

#설정 객체 생성 - 프로젝트 어디서든 불러올 수 있게
settings = Settings()