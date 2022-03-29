from unittest.mock import Mock

from kokon.functions.host import handle_get_all_hosts
from kokon.utils.db import DB

from tests.helpers import UserMock


def test_get_all_hosts(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"status": "CREATED"}

    response = handle_get_all_hosts(request)

    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert "email" in data[0]
