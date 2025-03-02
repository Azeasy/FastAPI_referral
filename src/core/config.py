from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFERRAL_DEFAULT_EXPIRY_DAYS: int

    class Config:
        env_file = ".env"


settings = Settings()
