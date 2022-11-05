# import pytest

# from typing import Dict

# from fastapi.testclient import TestClient

# from app.core.config import settings

# from typing import Dict, Generator


# from fastapi.testclient import TestClient
# from sqlalchemy.orm import Session

# from app.main import app
# from app.core.config import settings
# from app.database import database
# from app.models import models
# from app.crud import crud



# def test_register(
#     client: TestClient, 
#     superuser_token_headers: Dict[str, str]
#     ) -> None:

#     user = {}

#     r = client.post(
#         f"{settings.API_PREFIX}/register", 
#         json=user.dict(),
#         headers=superuser_token_headers,
#         )
    
#     new_user = r.json()
#     print(new_user)
#     assert r.status_code == 200
#     assert "username" in new_user
#     assert "email" in new_user
#     assert new_user['is_active']










