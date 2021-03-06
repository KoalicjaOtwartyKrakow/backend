import http
from unittest.mock import Mock, patch

from kokon.utils import authologic
from kokon.functions.host import (
    handle_add_host,
    handle_delete_host,
    handle_get_all_hosts,
    handle_get_host_by_id,
    handle_update_host,
    handle_registration,
)
from kokon.orm import Host, Language
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


def test_filter_by_language(db):
    with DB().acquire() as session:
        host = (
            session.query(Host)
            .where(Host.guid == "dc6d05bb-9bd6-4e9d-a8e9-8b88d29adee5")
            .one()
        )
        host.languages_spoken.append(Language(name="English", code2="EN", code3="Eng"))
        host.languages_spoken.append(
            Language(name="Ukrainian", code2="UK", code3="Ukr")
        )
        session.commit()

    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10, "languageSpoken": "EN"}

    response = handle_get_all_hosts(request)

    assert response.status_code == 200
    assert response.json["total"] == 1


def test_get_all_hosts_with_query_by_fullname(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"query": "królik", "limit": 10}

    response = handle_get_all_hosts(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert len(items) == 1
    assert "fullName" in items[0]
    assert items[0]["fullName"] == "Edmund Królikowski"


def test_get_all_hosts_with_query_by_phone(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"query": "143", "limit": 10}

    response = handle_get_all_hosts(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert len(items) == 1
    assert "phoneNumber" in items[0]
    assert items[0]["phoneNumber"] == "443 143 258"


def test_create_read_update_delete_host(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
    }
    response = handle_add_host(request)
    assert response.status_code == 201
    assert response.json["phoneNumber"] == "499-330-497"
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


@patch("kokon.functions.host.start_conversation")
def test_host_registration(test_patch):
    request = Mock()
    request.db = DB()
    test_patch.return_value = {
        "id": "782962fc-dc11-4a33-8f08-b7da532dd40d",
        "url": "http://take.me.there/",
    }
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.get_json.return_value = {
        "phoneNumber": "123123123",
        "fullName": "Marian Koniuszko",
        "email": "koniuszko@dummy.dum",
    }
    request.host_url = "http://dummy.dum/"

    response = handle_registration(request)

    assert response.status_code == 201
    assert response.get_json()["status"] == "CREATED"


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
