import secrets

from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl, BaseSettings, 
    HttpUrl, 
    PostgresDsn, validator
    )


class Settings(BaseSettings):

    API_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = secrets.token_urlsafe(32)

    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 60 minutes * 24 hours * 8 days = 8 days

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True,allow_reuse=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "notes-app"
    # SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl = "http://localhost"


    USE_POSTGRES_DB: bool = False
    POSTGRES_DB: Optional[str]
    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_HOST: Optional[str]
    POSTGRES_PORT: Optional[str]
    POSTGRES_PASSWORD: Optional[str]

    USE_SQLITE_DB: bool = True   
    SQLITE_DB: Optional[str] = "database.sqlite"

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgresserver/{DATABASE_NAME}"‘

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        elif values.get("USE_SQLITE_DB"):
            dbname=values.get("SQLITE_DB")
            return f"sqlite:///{dbname}"

        elif values.get("USE_POSTGRES_DB"):
            schema = values.get("POSTGRES_DB")
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD")
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT")
            return f'postgresql://{user}:{password}@{host}:{port}/{schema}'


    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = 'vitostamatti@gmail.com'
    FIRST_SUPERUSER_PASSWORD: str = "admin"


    class Config:
        case_sensitive = True


settings = Settings()