from sqlalchemy.orm import Session
from typing import Union, List
from app.models import models
from app.crud import crud
from app.core.config import settings

### Users
def test_get_users(db: Session) -> List[Union[models.User, None]]:
    users = crud.get_users(db)
    assert isinstance(users, list)


def test_get_user(db: Session) -> List[Union[models.User, None]]:
    user = crud.get_user(db, user_id=1)
    assert isinstance(user, models.User)


def test_get_user_by_username(db: Session) -> List[Union[models.User, None]]:
    user = crud.get_user_by_username(db, username=settings.FIRST_SUPERUSER)
    assert isinstance(user, models.User)
    assert user.username == settings.FIRST_SUPERUSER


def test_get_user_by_email(db: Session) -> List[Union[models.User, None]]:
    user = crud.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    assert isinstance(user, models.User)
    assert user.email == settings.FIRST_SUPERUSER_EMAIL
