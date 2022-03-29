from unittest.mock import Mock

from kokon.functions.accommodation import (
    handle_add_accommodation,
    handle_get_all_accommodations,
)
from kokon.utils.db import DB

from tests.helpers import UserMock


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


def test_get_all_accommodations(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")

    response = handle_get_all_accommodations(request)

    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]["voivodeship"] == "LUBELSKIE"
