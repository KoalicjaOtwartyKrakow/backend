import jwt
from unittest.mock import Mock

from utils import settings
from utils.functions import function_wrapper


@function_wrapper
def handle_example(request):
    assert request.user_guid
    return "ok"


def test_jwt_auth():
    request = Mock()
    request.headers = {"Authorization": ""}
    res = handle_example(request)
    assert res.status_code == 403

    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }
    jwt_encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    request.headers = {"Authorization": f"Bearer {jwt_encoded}"}
    res = handle_example(request)
    assert res == "ok"
