from sqlalchemy.orm import Session

from app.models import models
from app.database import database
from app.core.config import settings
from app.core.security import get_password_hash


def create_db_and_tables():
    models.Base.metadata.create_all(database.engine)


def drop_tables():
    models.Base.metadata.drop_all(database.engine)


def create_first_superuser(db: Session):
    if (
        not db.query(models.User)
        .filter(models.User.username == settings.FIRST_SUPERUSER)
        .first()
    ):
        db_user = models.User(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        db.add(db_user)
        db.commit()


def create_test_user(db: Session):
    if (
        not db.query(models.User)
        .filter(models.User.username == settings.TEST_USER)
        .first()
    ):
        db_user = models.User(
            username=settings.TEST_USER,
            email=settings.TEST_USER_EMAIL,
            hashed_password=get_password_hash(settings.TEST_USER_PASSWORD),
            is_superuser=False,
        )
        db.add(db_user)
        db.commit()


def init():
    create_db_and_tables()
    with database.SessionMaker() as db:
        create_first_superuser(db)
        create_test_user(db)


def reset():
    drop_tables()
