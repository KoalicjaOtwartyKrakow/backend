import jwt

from utils.auth import upsert_user_from_jwt
from utils.db import DB
from utils import settings


def test_upsert_user_from_jwt():
    db = DB()
    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    jwt_encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    res = upsert_user_from_jwt(db, jwt_encoded)

    assert res

    res2 = upsert_user_from_jwt(db, jwt_encoded)

    assert res2 == res
