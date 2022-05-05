import uuid
import pytest

from kokon.settings import AUTHOLOGIC_URL, AUTHOLOGIC_USER, AUTHOLOGIC_PASS
from kokon.utils.authologic import start_conversation


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


@pytest.mark.integtest
def test_start_conversation():
    assertion_error = 'You need to setup {} env variable or skip integration tests: pytest tests -m "not integtest"'
    assert AUTHOLOGIC_URL, assertion_error.format("AUTHOLOGIC_URL")
    assert AUTHOLOGIC_USER, assertion_error.format("AUTHOLOGIC_USER")
    assert AUTHOLOGIC_PASS, assertion_error.format("AUTHOLOGIC_PASS")

    response = start_conversation(str(uuid.uuid4()), "http://dummy.dum/")

    assert is_valid_uuid(response["id"])
    assert response["url"]
