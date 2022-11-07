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

from tests.utils import get_random_note, random_lower_string


def test_get_notes(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:

    r = client.get(
        f"{settings.API_PREFIX}/notes/?skip=0&limit=100",
        headers=normal_user_token_headers,
    )

    result = r.json()
    assert r.status_code == 200
    assert isinstance(result, list)


def test_create_note(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    new_note = get_random_note()
    r = client.post(
        f"{settings.API_PREFIX}/notes/",
        json=new_note.dict(exclude_unset=True),
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result["name"] == new_note.name
    assert result["content"] == new_note.content


def test_get_note_by_id(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:

    r = client.get(
        f"{settings.API_PREFIX}/notes/1",
        headers=normal_user_token_headers,
    )
    result = r.json()
    print(result)
    assert r.status_code == 200
    assert result["id"] == 1


def test_update_note(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:
    new_name = random_lower_string()
    note = schemas.NoteUpdate(name=new_name)
    r = client.put(
        f"{settings.API_PREFIX}/notes/1",
        json=note.dict(exclude_unset=True),
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert result["name"] == new_name


def test_delete_note(
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:

    r = client.delete(
        f"{settings.API_PREFIX}/notes/1",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
