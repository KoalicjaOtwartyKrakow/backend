import jwt
from unittest.mock import Mock

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from utils.functions import function_wrapper


@function_wrapper
def handle_example(request):
    assert request.user_guid
    return "ok"


def test_jwt_auth__missing():
    request = Mock()
    request.headers = {"Authorization": ""}
    res = handle_example(request)
    assert res.status_code == 403
    assert res.json == {"message": "Not authenticated."}


def test_jwt_auth__ok():
    request = Mock()

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

    request.headers = {"Authorization": f"Bearer {jwt_encoded}"}
    res = handle_example(request)
    assert res == "ok"
