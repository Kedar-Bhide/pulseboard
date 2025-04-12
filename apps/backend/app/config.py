from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()