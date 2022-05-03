import base64
import json

from unittest.mock import Mock

from kokon.utils.db import DB
from kokon.utils.functions import function_wrapper


@function_wrapper
def handle_example(request):
    assert request.user.email
    assert isinstance(request.db, DB)
    return "ok"


@function_wrapper(public=True)
def handle_example_public(request):
    assert isinstance(request.db, DB)
    return "ok"


def test_jwt_auth__missing():
    request = Mock()
    request.headers = {"X-Endpoint-API-UserInfo": ""}
    res = handle_example(request)
    assert res.status_code == 401
    assert res.json == {"message": "Unauthorized."}


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


def test_jwt_auth__unauthorized():
    request = Mock()

    # Authorized_emails are listed in settings,
    # see pytest.ini for list of emails authorized for tests.
    payload = {
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@another.com",
        "sub": "10769150350006150715113082367",
        "picture": "https://google.com/123",
    }

    request.headers = {
        "X-Endpoint-API-UserInfo": base64.urlsafe_b64encode(
            json.dumps(payload).encode("utf-8")
        )
    }
    res = handle_example(request)
    assert res.status_code == 401
    assert res.json == {"message": "Unauthorized."}


def test_no_jwt_auth_required_in_public_endpoint():
    request = Mock()
    res = handle_example_public(request)
    assert res == "ok"
