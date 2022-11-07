import random
from sqlalchemy.orm import Session
from typing import Dict
from fastapi.testclient import TestClient
import string

from app.models import models
from app.core.config import settings
from app.crud import crud
from app.schemas import schemas


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_username() -> str:
    return f"{random_lower_string()}"


def get_superuser_authentication_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_user_authentication_headers(client: TestClient) -> Dict[str, str]:

    data = {"username": settings.TEST_USER, "password": settings.TEST_USER_PASSWORD}

    r = client.post(f"{settings.API_PREFIX}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_random_user() -> schemas.UserCreate:
    return schemas.UserCreate(
        username=random_username(), email=random_email(), password=random_lower_string()
    )


def create_random_user(db: Session) -> schemas.UserCreate:
    email = random_email()
    username = random_username()
    password = random_lower_string()
    user_in = schemas.UserCreate(username=username, email=email, password=password)
    user = crud.create_user(db, user_in)
    return user


def get_random_note() -> schemas.NoteCreate:
    return schemas.NoteCreate(name=random_lower_string(), content=random_lower_string())
