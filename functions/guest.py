"""Module containing function handlers for guest requests."""

import flask

from sqlalchemy import exc, select

from utils.db import get_db_session
from utils.orm import Guest
from utils.payload_parser import parse, GuestParser, is_valid_uuid


def handle_get_all_guests(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(Guest)
        result = session.execute(stmt)
        response = [guest.to_json() for guest in result.scalars()]
    return flask.Response(response=response, status=200)


def handle_add_guest(request):
    data = request.get_json()
    result = parse(data, GuestParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status=400)

    return flask.Response(status=201)


def handle_get_guest_by_id(request):
    value = request.path.split("/")
    guest_id = value[2]

    if not is_valid_uuid(guest_id):
        return flask.Response(
            response=f"Received invalid guestId: {guest_id}", status=405
        )

    Session = get_db_session()
    with Session() as session:
        try:
            stmt = select(Guest).where(Guest.guid == guest_id)
            result = session.execute(stmt)
            response = [guest.to_json() for guest in result.scalars()]
            if response is None:
                return flask.Response(
                    response=f"Guest with id = {guest_id} not found", status=404
                )

            return flask.Response(response=response, status=200)
        except TypeError as e:
            return flask.Response(response=f"Received invalid guestId: {e}", status=405)


def handle_delete_guest(request):
    value = request.path.split("/")
    guest_id = value[2]

    if not is_valid_uuid(guest_id):
        return flask.Response(
            response=f"Received invalid guestId: {guest_id}", status=405
        )

    Session = get_db_session()
    try:
        with Session() as session:
            result1 = (
                session.query(Guest)
                .filter(Guest.guid == guest_id)
                .delete(synchronize_session=False)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")
    except exc.SQLAlchemyError as e:
        return flask.Response(f"delete_guest unsuccessful e: {e}", status=400)

    return flask.Response(status=200)


def handle_update_guest(request):
    value = request.path.split("/")
    guest_id = value[2]

    if not is_valid_uuid(guest_id):
        return flask.Response(
            response=f"Received invalid guestId: {guest_id}", status=405
        )

    request_json = request.get_json()
    print(request_json)
    Session = get_db_session()
    try:
        with Session() as session:
            result1 = (
                session.query(Guest).filter(Guest.guid == guest_id).update(request_json)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")
    except exc.SQLAlchemyError as e:
        return flask.Response(f"update_guest unsuccessful e: {e}", status=400)

    return flask.Response(status=200)
