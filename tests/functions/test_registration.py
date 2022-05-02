import http
from unittest.mock import Mock

from kokon.functions.host import handle_registration

from kokon.utils.db import DB

from tests.helpers import UserMock


def test_get_all_hosts(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {
        "phoneNumber": "123123123",
        "fullName": "Marian Koniuszko",
        "email": "koniuszko@dummy.dum",
    }

    response = handle_registration(request)

    assert response.status_code == 201  # TODO: assertions
