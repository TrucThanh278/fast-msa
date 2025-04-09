from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_HOST: str = "http://localhost:8000"

    PROJECT_NAME: str = "movie_service"
    DEBUG: bool = True

    POSTGRES_USER: str = "movie_db_username"
    POSTGRES_PASSWORD: str = "movie_db_password"
    POSTGRES_SERVER: str = "movie_db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB_NAME: str = "movie_db_dev"

    def SQLALCHEMY_DATABASE_URI(self):
        uri = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"
        return uri


settings = Settings()
