import secrets

from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
import os

class Settings(BaseSettings):

    API_PREFIX: str = "/api"
    PROJECT_NAME: str = 'notes-app'
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 8
    )  # 60 minutes * 24 hours * 8 days = 8 days

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    USE_POSTGRES_DB: bool = os.environ.get('USE_POSTGRES_DB',True) 
    POSTGRES_DB: Optional[str] = os.environ.get("POSTGRES_DB","db")
    POSTGRES_USER: Optional[str] = os.environ.get("POSTGRES_USER","admin")
    POSTGRES_HOST: Optional[str] = os.environ.get("POSTGRES_HOST","0.0.0.0")
    POSTGRES_PORT: Optional[str] = os.environ.get("POSTGRES_PORT","5432")
    POSTGRES_PASSWORD: Optional[str] = os.environ.get("POSTGRES_PASSWORD","admin")

    USE_SQLITE_DB: bool = False
    SQLITE_DB: Optional[str] = "database.sqlite"

    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    if USE_SQLITE_DB:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB}"
    elif USE_POSTGRES_DB:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        print(SQLALCHEMY_DATABASE_URI)

    # DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgresserver/{DATABASE_NAME}"‘

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v

    #     elif values.get("USE_SQLITE_DB"):
    #         dbname = values.get("SQLITE_DB")
    #         return f"sqlite:///{dbname}"

    #     elif values.get("USE_POSTGRES_DB"):
    #         schema = values.get("POSTGRES_DB")
    #         user = values.get("POSTGRES_USER")
    #         password = values.get("POSTGRES_PASSWORD")
    #         host = values.get("POSTGRES_HOST")
    #         port = values.get("POSTGRES_PORT")
    #         return f"postgresql://{user}:{password}@{host}:{port}/{schema}"

    FIRST_SUPERUSER: str = os.environ.get('FIRST_SUPERUSER',"admin") 
    FIRST_SUPERUSER_EMAIL: str =  os.environ.get('FIRST_SUPERUSER_EMAIL',"admin@domain.com")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get('FIRST_SUPERUSER_PASSWORD',"admin") 

    TEST_USER: str = "user"
    TEST_USER_EMAIL: str = "user@domain.com"
    TEST_USER_PASSWORD: str = "user"

    class Config:
        case_sensitive = True


settings = Settings()
