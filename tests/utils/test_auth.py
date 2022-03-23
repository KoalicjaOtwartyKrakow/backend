import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from utils.auth import upsert_user_from_jwt
from utils.db import DB


def test_upsert_user_from_jwt__no_change():
    db = DB()
    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    jwt_encoded = jwt.encode(
        payload,
        rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        ),
        algorithm="RS256",
    )
    user = upsert_user_from_jwt(db, jwt_encoded)

    assert user

    user_again = upsert_user_from_jwt(db, jwt_encoded)

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
    jwt_encoded_one = jwt.encode(
        payload_one,
        rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        ),
        algorithm="RS256",
    )
    user = upsert_user_from_jwt(db, jwt_encoded_one)

    assert user

    payload_two = {
        "given_name": "Johnny",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    jwt_encoded_two = jwt.encode(
        payload_two,
        rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        ),
        algorithm="RS256",
    )

    user_changed = upsert_user_from_jwt(db, jwt_encoded_two)

    assert user_changed.guid == user.guid
    assert user_changed.given_name != user.given_name
    assert user_changed.given_name == "Johnny"
