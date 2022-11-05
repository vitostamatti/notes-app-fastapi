import pytest

from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings

from typing import Dict, Generator


from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.database import database
from app.models import models


from tests.utils import (
    create_random_user,
    get_superuser_authentication_headers,
    get_user_authentication_headers,
    get_random_user
    )



def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    print(tokens)
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, 
    superuser_token_headers: Dict[str, str]
    ) -> None:

    r = client.post(
        f"{settings.API_PREFIX}/login/test-token", 
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "username" in result


def test_register(
    client: TestClient, 
    superuser_token_headers: Dict[str, str]
    ) -> None:

    user = get_random_user()
    print(user.dict())
    r = client.post(
        f"{settings.API_PREFIX}/register", 
        json=user.dict(),
        headers=superuser_token_headers,
        )
    
    new_user = r.json()
    print(new_user)
    assert r.status_code == 200
    assert "username" in new_user
    assert "email" in new_user
    assert new_user['is_active']










