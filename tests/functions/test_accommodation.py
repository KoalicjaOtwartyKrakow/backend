import http
from unittest.mock import Mock

from kokon.functions.accommodation import (
    handle_add_accommodation,
    handle_delete_accommodation,
    handle_get_accommodation_by_id,
    handle_get_all_accommodations,
    handle_update_accommodation,
    handle_public_add_accommodation,
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


def test_self_create_accommodations(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "9449e8d2-d0f8-455e-a181-1f35616d107d"}
    request.get_json.return_value = [
        {
            "vacanciesTotal": 1,
            "zip": "12345",
            "addressLine": "Address 1",
        },
        {
            "vacanciesTotal": 1,
            "zip": "12345",
            "addressLine": "Address 2",
        },
    ]
    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.CREATED
    assert [accommodation["addressLine"] for accommodation in response.json] == [
        "Address 1",
        "Address 2",
    ]
    assert [accommodation["hostId"] for accommodation in response.json] == [
        "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
        "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5",
    ]


def test_self_create_accommodations_for_the_second_time_fails(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "9449e8d2-d0f8-455e-a181-1f35616d107d"}
    request.get_json.return_value = [
        {
            "vacanciesTotal": 1,
            "zip": "12345",
            "addressLine": "Address 1",
        }
    ]
    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.CREATED
    request.get_json.return_value = [
        {
            "vacanciesTotal": 1,
            "zip": "12345",
            "addressLine": "Address 2",
        }
    ]
    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.CONFLICT


def test_self_create_accommodations_missing_conversation_id_parameter(db):
    request = Mock()
    request.db = DB()
    request.args = {}

    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_self_create_accommodations_invalid_conversation_id_parameter(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "invalidUUID"}

    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_self_create_accommodations_not_found_conversation(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "882962fc-dc11-4a33-8f08-b7da532dd40d"}

    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_self_create_accommodations_single_element_instead_of_list(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "9449e8d2-d0f8-455e-a181-1f35616d107d"}
    request.get_json.return_value = {
        "vacanciesTotal": 1,
        "zip": "12345",
        "addressLine": "Address 2",
    }
    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.CREATED


def test_self_create_accommodations_missing_parameters(db):
    request = Mock()
    request.db = DB()
    request.args = {"conversationId": "9449e8d2-d0f8-455e-a181-1f35616d107d"}
    request.get_json.return_value = [
        {"vacanciesTotal": 1, "zip": "12345"},
    ]
    response = handle_public_add_accommodation(request)
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
