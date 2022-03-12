# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import flask
import functions_framework

from sqlalchemy import exc, select
from utils.db import get_db_session

from utils import orm
from functions import handle_create_host


@functions_framework.http
def add_accommodation(request):
    """HTTP Cloud Function for posting new accommodation units."""
    # parse request
    request_json = request.get_json()

    # create Apartment object from json
    try:
        apartment = orm.AccommodationUnit(**request_json)
    except TypeError as e:
        return flask.Response(
            response=f"Received invalid parameter(s) for apartment: {e}", status=405
        )

    Session = get_db_session()
    with Session() as session:
        session.add(apartment)
        # db transaction
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status = 400)

        return flask.Response(status=200)


@functions_framework.http
def get_all_accommodations(request):
    """HTTP Cloud Function for getting all available accommodation units."""
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.AccommodationUnit)
        return session.execute(stmt)


@functions_framework.http
def delete_apartment(request):
    """HTTP Cloud Function for deleting apartment."""


@functions_framework.http
def create_host(request):
    return handle_create_host(request)


@functions_framework.http
def get_all_guests(request):
    """HTTP Cloud Function for getting all guests."""
    Session = get_db_session()
    session = Session()

    stmt = select(orm.Guest)
    result = session.execute(stmt)

    print(result)

    return flask.Response(status=200)

@functions_framework.http
def add_guest(request):
    """HTTP Cloud Function for posting new guests."""
    # parse request
    request_json = request.get_json()

    # create Guest object from json
    try:
        guest = orm.Guest(**request_json)
    except TypeError as e:
        return flask.Response(response=f"Received invalid parameter(s) for guest: {e}", status = 405)

    Session = get_db_session()
    with Session() as session:
        session.add(guest)
        # db transaction
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status = 400)

        return flask.Response(status=201)

@functions_framework.http
def get_guest_by_id(request):
    """HTTP Cloud Function for getting guest by id."""

    id = request.args.get('guestId')
    if id is None or not id.isdigit():
        return flask.Response(response=f"Received invalid guestId: {id}", status = 405)

    Session = get_db_session()
    with Session() as session:
        try:
            guest = session.query(orm.Guest).get(id)
            if guest is None:
                return flask.Response(response=f"Guest with id = {id} not found", status = 404)

            return flask.Response(response=guest.toJSON(), status = 200)

        except TypeError as e:
            return flask.Response(response=f"Received invalid guestId: {e}", status = 405)
