"""Module containing function handlers for guest requests."""

import flask
import flask
from sqlalchemy import exc, select
from utils.db import get_db_session
from utils import orm


def handle_get_all_guests(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Guest)
        result = session.execute(stmt)
        response = [guest.to_json() for guest in result.scalars()]

    return flask.Response(response=response, status=200)

def handle_add_guest(request):
    request_json = request.get_json()
    try:
        guest = orm.Guest(**request_json)
    except TypeError as e:
        return flask.Response(
            response=f"Received invalid parameter(s) for guest: {e}", status=405
        )

    Session = get_db_session()
    with Session() as session:
        session.add(guest)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status=400)

    return flask.Response(status=201)

def handle_get_guest_by_id(request):
    id = request.args.get('guestId')
    if id is None or not id.isdigit():
        return flask.Response(response=f"Received invalid guestId: {id}", status = 405)

    Session = get_db_session()
    with Session() as session:
        try:
            guest = session.query(orm.Guest).get(id)
            if guest is None:
                
                return flask.Response(response=f"Guest with id = {id} not found", status = 404)

            return flask.Response(response=guest.to_json(), status = 200)
        except TypeError as e:

            return flask.Response(response=f"Received invalid guestId: {e}", status = 405)

