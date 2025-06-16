from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import Environment


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
        case_sensitive=True,
    )

    ENVIRONMENT: Environment = Environment.LOCAL
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    API_PREFIX: str = '/api/v1'
    JWT_ALGORITHM: str = 'HS512'
    JWT_EXPIRATION: int = 1
    JWT_ISSUER: str = 'fastapi-jwt-auth'
    JWT_AUDIENCE: str = 'fastapi-jwt-auth'


settings: Settings = Settings()  # type: ignore
