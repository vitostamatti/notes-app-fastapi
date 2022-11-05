import pytest

from typing import Dict

from fastapi.testclient import TestClient

from typing import Dict, Generator

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import database
from app.models import models


from tests.utils import (
    create_random_user,
    get_superuser_authentication_headers,
    get_user_authentication_headers,
    )


@pytest.fixture(scope="session")
def db() -> Generator:
    yield database.SessionMaker()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_authentication_headers(client)


@pytest.fixture(scope="session")
def user_test(client: TestClient) -> models.User:
    return create_random_user()


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return get_user_authentication_headers(client=client, user=user_test)
