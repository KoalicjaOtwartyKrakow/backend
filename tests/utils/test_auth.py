import base64
import json

from kokon.utils.auth import upsert_user_from_jwt
from kokon.utils.db import DB


def test_upsert_user_from_jwt__no_change():
    db = DB()
    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8"))
    user = upsert_user_from_jwt(db, payload_encoded)

    assert user

    user_again = upsert_user_from_jwt(db, payload_encoded)

    assert user_again.guid == user.guid


def test_upsert_user_from_jwt__name_changed():
    db = DB()
    payload_one = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    payload_one_encoded = base64.urlsafe_b64encode(
        json.dumps(payload_one).encode("utf-8")
    )
    user = upsert_user_from_jwt(db, payload_one_encoded)

    assert user

    payload_two = {
        "given_name": "Johnny",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    payload_two_encoded = base64.urlsafe_b64encode(
        json.dumps(payload_two).encode("utf-8")
    )
    user_changed = upsert_user_from_jwt(db, payload_two_encoded)

    assert user_changed.guid == user.guid
    assert user_changed.given_name != user.given_name
    assert user_changed.given_name == "Johnny"
