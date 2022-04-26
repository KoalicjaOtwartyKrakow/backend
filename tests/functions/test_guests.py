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
from kokon.utils.db import DB
from kokon.orm import Guest

from tests.helpers import UserMock


def test_get_all_guests(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10}

    response = handle_get_all_guests(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert items[0]["email"] == "gsssltitzwwg@gmail.com"


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

    with DB().acquire() as session:
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


def test_edit_guest_with_immutable_fields_ignores_them(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")

    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "phoneNumber": "499-330-497",
        "childrenAges": [1, 10],
    }

    response_add = handle_add_guest(request)
    assert response_add.status_code == http.HTTPStatus.CREATED
    guest_guid = response_add.json["guid"]

    request.args = {"guestId": guest_guid}

    # immutable fields present in full serializer
    immutable_fields = {
        "guid": "182962fc-dc11-4a33-8f08-b7da532dd40d",
        "createdAt": "2022-04-24 10:52:42.283345",
        # "updatedAt" is skipped on purpose, because it will always differ (it is imposed by SQL engine)
        "updatedBy": "182962fc-dc11-4a33-8f08-b7da532dd40d",
        "claimedAt": "2022-04-24 10:52:42.283345",
        "accommodationUnit": "i will be ignored",
    }

    # immutable fields not present in full serializer
    internal_immutable_fields = {
        "updatedById": "182962fc-dc11-4a33-8f08-b7da532dd40d",
        "versions": None,
    }
    request.get_json.return_value = {
        "fullName": "Marta Andrzejak",
        "phoneNumber": "499-330-497",
        "childrenAges": [1, 10],
        # fields supposed to be immutable, so expected behavior is to ignore them on update
        **immutable_fields,
        **internal_immutable_fields,
    }
    response_update = handle_update_guest(request)

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

    # we also want to check if history of internal immutable fields is not tampered by an update request
    # NOTE: "versions" is also an immutable fields, and an assumption is made, that if it would be
    # tampered by an update request, the below assertions would not pass anyway
    with DB().acquire() as session:
        version_cls = version_class(Guest)
        versions = session.execute(
            sa.select(version_cls).where(version_cls.guid == guest_guid)
        ).all()
        expected_updated_by_id_history = [
            "782962fc-dc11-4a33-8f08-b7da532dd40d",
            "782962fc-dc11-4a33-8f08-b7da532dd40d",
        ]
        assert [
            str(v[0].updated_by_id) for v in versions
        ] == expected_updated_by_id_history
