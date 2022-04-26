import http
from unittest.mock import Mock

from kokon.functions.accommodation import (
    handle_add_accommodation,
    handle_delete_accommodation,
    handle_get_accommodation_by_id,
    handle_get_all_accommodations,
    handle_update_accommodation,
)
from kokon.utils.db import DB

from tests.helpers import UserMock


def test_get_all_accommodations(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10}

    response = handle_get_all_accommodations(request)

    assert response.status_code == 200
    data = response.json
    assert data["total"] == 1
    items = data["items"]
    assert items[0]["voivodeship"] == "LUBELSKIE"
    assert items[0]["host"]["status"] == "CREATED"
    assert len(items[0]["guests"]) == 1


def test_create_read_update_delete_accommodation(db):
    request = Mock()
    request.db = DB()
    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12345",
        "hostId": "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "addressLine": "Address 1",
    }
    response = handle_add_accommodation(request)
    assert response.status_code == 201
    assert response.json["zip"] == "12345"
    assert response.json["verificationStatus"] == "CREATED"
    accommodation_guid = response.json["guid"]

    request.args = {"accommodationId": accommodation_guid}
    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12346",
        "hostId": "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "addressLine": "Address 1",
    }
    response = handle_update_accommodation(request)
    assert response.status_code == 200
    assert response.json["zip"] == "12346"

    response = handle_get_accommodation_by_id(request)
    assert response.status_code == 200
    assert response.json["zip"] == "12346"

    response = handle_delete_accommodation(request)
    assert response.status_code == 204


def test_get_edit_delete_accommodation_missing_accommodation_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {}

    response = handle_get_accommodation_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_accommodation(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_accommodation(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_accommodation_invalid_accommodation_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"accommodationId": "invalidUUID"}

    response = handle_get_accommodation_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_accommodation(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_accommodation(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_accommodation_not_found_accommodation():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"accommodationId": "882962fc-dc11-4a33-8f08-b7da532dd40d"}

    response = handle_get_accommodation_by_id(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_update_accommodation(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_delete_accommodation(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_edit_accommodation_with_immutable_fields_ignores_them(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")

    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12345",
        "hostId": "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "addressLine": "Address 1",
    }

    response_add = handle_add_accommodation(request)
    assert response_add.status_code == http.HTTPStatus.CREATED
    accommodation_guid = response_add.json["guid"]

    request.args = {"accommodationId": accommodation_guid}

    # immutable fields present in full serializer
    immutable_fields = {
        "guid": "182962fc-dc11-4a33-8f08-b7da532dd40d",
        "createdAt": "2022-04-24 10:52:42.283345",
        # "updatedAt" is skipped on purpose, because it will always differ (it is imposed by SQL engine)
        "host": None,
        "guests": None,
    }

    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12345",
        "hostId": "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "addressLine": "Address 1",
        # fields supposed to be immutable, so expected behavior is to ignore them on update
        **immutable_fields,
    }
    response_update = handle_update_accommodation(request)

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
