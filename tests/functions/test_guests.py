import http
from unittest.mock import Mock

import sqlalchemy as sa
from sqlalchemy_continuum.utils import version_class

from kokon.functions.guest import (
    handle_add_guest,
    handle_delete_guest,
    handle_get_all_guests,
    handle_get_guest_by_id,
    handle_update_guest,
)
from kokon.orm import Guest
from kokon.utils.db import DB

from tests.helpers import UserMock, admin_session


def test_get_all_guests(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10}

    response = handle_get_all_guests(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert items[0]["email"] == "gsssltitzwwg@gmail.com"


def test_guest_filters(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10, "priorityStatus": "DOES_NOT_RESPOND"}

    response = handle_get_all_guests(request)

    assert response.status_code == 200
    assert response.json["total"] == 0

    request.args = {"limit": 10, "priorityStatus": "EN_ROUTE_PL"}

    response = handle_get_all_guests(request)

    assert response.status_code == 200
    assert response.json["total"] == 1


def test_create_edit_delete_guest_versions(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
        "childrenAges": [1, 10],
    }

    response = handle_add_guest(request)
    assert response.status_code == 201
    guest_guid = response.json["guid"]

    request.user = UserMock(guid="46389922-28b5-430f-a2e1-04fcddd70117")
    request.args = {"guestId": guest_guid}
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "email": "auz-oxloij-dxfv@yahoo.com",
        "phoneNumber": "499-330-497",
        "childrenAges": [1, 10],
        "accommodationUnitId": "008c0243-0060-4d11-9775-0258ddac7620",
    }

    response = handle_update_guest(request)
    assert response.status_code == 200

    response = handle_get_guest_by_id(request)
    assert response.status_code == 200
    assert response.json["fullName"] == "Marta Andrzejak"

    request.get_json.return_value = {}
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    response = handle_delete_guest(request)
    assert response.status_code == 204

    with admin_session() as session:
        version_cls = version_class(Guest)
        versions = session.execute(
            sa.select(version_cls)
            .where(version_cls.guid == guest_guid)
            .order_by(version_cls.updated_at)
        ).all()
        assert [str(v[0].updated_by_id) for v in versions] == [
            "782962fc-dc11-4a33-8f08-b7da532dd40d",
            "46389922-28b5-430f-a2e1-04fcddd70117",
            "782962fc-dc11-4a33-8f08-b7da532dd40d",
            "782962fc-dc11-4a33-8f08-b7da532dd40d",
        ]


def test_get_edit_delete_guest_missing_guest_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {}

    response = handle_get_guest_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_guest(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_guest(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_guest_invalid_guest_id_parameter():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"guestId": "invalidUUID"}

    response = handle_get_guest_by_id(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_update_guest(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = handle_delete_guest(request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_edit_delete_guest_not_found_guest():
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"guestId": "882962fc-dc11-4a33-8f08-b7da532dd40d"}

    response = handle_get_guest_by_id(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_update_guest(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

    response = handle_delete_guest(request)
    assert response.status_code == http.HTTPStatus.NOT_FOUND
