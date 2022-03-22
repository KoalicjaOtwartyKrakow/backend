import jwt

from repos.users import UsersRepo
from utils.db import DB
from utils import settings


def test_upsert_from_jwt():
    repo = UsersRepo(DB())
    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    jwt_encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    res = repo.upsert_from_jwt(jwt_encoded)

    assert res == {
        "email": "john.doe@example.com",
        "family_name": "Doe",
        "given_name": "John",
        "google_picture": "https://google.com/123",
        "google_sub": "10769150350006150715113082367",
        "guid": res["guid"],
    }

    res2 = repo.upsert_from_jwt(jwt_encoded)

    assert res2["guid"] == res["guid"]
