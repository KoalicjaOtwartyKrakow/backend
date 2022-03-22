import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from utils.auth import upsert_user_from_jwt
from utils.db import DB


def test_upsert_user_from_jwt():
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
    res = upsert_user_from_jwt(db, jwt_encoded)

    assert res

    res2 = upsert_user_from_jwt(db, jwt_encoded)

    assert res2 == res
