# import pytest

# from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings

from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# from app.main import app
# from app.core.config import settings
# from app.database import database
from app.models import models
from app.schemas import schemas
from app.crud import crud

from tests.utils import create_random_user, random_email, random_username


def test_get_users(
    client: TestClient, superuser_token_headers: Dict[str, str], db
) -> None:
    r = client.get(
        f"{settings.API_PREFIX}/user/?skip=0&limit=100",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert isinstance(result, list)


def test_get_user_by_id(
    client: TestClient, superuser_token_headers: Dict[str, str], db
) -> None:

    r = client.get(
        f"{settings.API_PREFIX}/user/1",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result["id"] == 1


def test_get_active_user(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
) -> None:

    r = client.get(
        f"{settings.API_PREFIX}/user/profile",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result["id"] == 1


def test_update_active_user(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:

    new_email = random_email()
    user_in = schemas.UserUpdate(email=new_email)
    r = client.put(
        f"{settings.API_PREFIX}/user/profile",
        json=user_in.dict(exclude_unset=True),
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result["email"] == new_email


def test_update_user(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    db: Session,
) -> None:

    test_user = crud.get_user_by_username(db, username=settings.TEST_USER)

    new_email = random_email()
    user_in = schemas.UserUpdate(email=new_email)

    r = client.put(
        f"{settings.API_PREFIX}/user/{test_user.id}",
        json=user_in.dict(exclude_unset=True),
        headers=superuser_token_headers,
    )
    result = r.json()
    print(result)
    assert r.status_code == 200
    assert result["email"] == new_email


def test_delete_user(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    db: Session,
) -> None:

    new_user = schemas.UserCreate(
        username=random_username(), email=random_email(), password="1234"
    )
    crud.create_user(db, user=new_user)
    db_user = crud.get_user_by_username(db, new_user.username)

    r = client.delete(
        f"{settings.API_PREFIX}/user/{db_user.id}",
        headers=superuser_token_headers,
    )
    result = r.json()
    print(result)
    assert r.status_code == 200
