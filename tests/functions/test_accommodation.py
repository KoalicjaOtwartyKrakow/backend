from unittest.mock import Mock

from kokon.functions.accommodation import handle_add_accommodation
from kokon.utils.db import DB


def test_add_accommodation(db):
    request = Mock()
    request.db = DB()
    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12345",
        "hostId": "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "addressLine": "Address 1",
    }
    response = handle_add_accommodation(request)
    assert response.json["status"] == "CREATED"
