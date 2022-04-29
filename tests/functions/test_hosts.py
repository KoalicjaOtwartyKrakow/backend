import http
from unittest.mock import Mock

import pytest

from kokon.functions.host import (
    handle_add_host,
    handle_delete_host,
    handle_get_all_hosts,
    handle_get_host_by_id,
    handle_update_host,
)
from kokon.utils.db import DB

from tests.helpers import UserMock


def test_get_all_hosts(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"status": "CREATED", "limit": 10}

    response = handle_get_all_hosts(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert len(items) == 2
    assert "email" in items[0]


def test_create_read_update_delete_host(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
        "languagesSpoken": [{"code2": "en"}],
    }
    response = handle_add_host(request)
    assert response.status_code == 201
    assert response.json["phoneNumber"] == "499-330-497"
    assert response.json["languagesSpoken"] == [
        {"name": "English", "code2": "en", "code3": "eng"}
    ]
    host_guid = response.json["guid"]

    request.args = {"hostId": host_guid}
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-498",
    }
    response = handle_update_host(request)
    assert response.status_code == 200
    assert response.json["phoneNumber"] == "499-330-498"

    response = handle_get_host_by_id(request)
    assert response.status_code == 200
    assert response.json["fullName"] == "Marta Andrzejak"

    response = handle_delete_host(request)
    assert response.status_code == 204


def test_get_edit_delete_host_missing_host_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {}

    response = handle_get_host_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_host(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_host(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_host_invalid_host_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"hostId": "invalidUUID"}

    response = handle_get_host_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_host(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_host(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_host_not_found_host():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"hostId": "882962fc-dc11-4a33-8f08-b7da532dd40d"}

    response = handle_get_host_by_id(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_update_host(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_delete_host(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@pytest.mark.xfail(
    reason="we need to use HostSchema (instead of HostSchemaFull)"
    " for loading data, to exclude immutable fields"
)
def test_edit_host_with_immutable_fields_ignores_them(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")

    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
    }

    response_add = handle_add_host(request)
    assert response_add.status_code == http.HTTPStatus.CREATED
    host_guid = response_add.json["guid"]

    request.args = {"hostId": host_guid}

    # immutable fields present in full serializer
    immutable_fields = {
        "guid": "182962fc-dc11-4a33-8f08-b7da532dd40d",
        "createdAt": "2022-04-24 10:52:42.283345",
        # "updatedAt" is skipped on purpose, because it will always differ (it is imposed by SQL engine)
        "accommodationUnits": "i will be ignored",
    }

    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
        # fields supposed to be immutable, so expected behavior is to ignore them on update
        **immutable_fields,
    }
    response_update = handle_update_host(request)

    assert response_update.status_code == http.HTTPStatus.OK

    # since we ignored immutable fields,
    # we expect that all fields we provided in an update request
    # are exactly the same in both create and update responses
    assert all(
        [
            response_add.json[field] == response_update.json[field]
            # we don't check internal immutable fields, as they are not present in response JSON
            for field in immutable_fields.keys()
        ]
    )


def test_create_host_with_invalid_language(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
        "languagesSpoken": [{"code2": "xy"}],
    }
    response = handle_add_host(request)
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
