from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:3000","http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()


