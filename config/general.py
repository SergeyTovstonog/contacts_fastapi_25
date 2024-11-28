from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_test_url: str
    secret_key: str
    mail_username: str = "test"
    mail_password: str = "test"
    mail_from: str = "admin@25web.com"
    mail_port: int = 1025
    mail_server: str = "localhost"
    redis_url: str = "redis://redis:6379"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
