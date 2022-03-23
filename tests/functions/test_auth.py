import base64
import json

from unittest.mock import Mock

from utils.functions import function_wrapper


@function_wrapper
def handle_example(request):
    assert request.user_guid
    return "ok"


def test_jwt_auth__missing():
    request = Mock()
    request.headers = {"X-Endpoint-API-UserInfo": ""}
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

    request.headers = {
        "X-Endpoint-API-UserInfo": base64.urlsafe_b64encode(
            json.dumps(payload).encode("utf-8")
        )
    }
    res = handle_example(request)
    assert res == "ok"
