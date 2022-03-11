# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import flask
import functions_framework

from sqlalchemy import exc, select
from utils.db import get_db_session

from utils import orm
from functions.create_host import handle_create_host


@functions_framework.http
def add_accommodation(request):
    """HTTP Cloud Function for posting new accommodation units."""
    # parse request
    request_json = request.get_json()

    # create Apartment object from json
    try:
        apartment = orm.AccommodationUnit(**request_json)
    except TypeError as e:
        return f"Received invalid parameter(s) for apartment: {e}", 405

    Session = get_db_session()
    with Session() as session:
        session.add(apartment)
        # db transaction
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return (f"Transaction error: {e}", 400)

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

    return {}, 200


@functions_framework.http
def get_all_hosts(request):
    """HTTP Cloud Function for getting all hosts."""
    Session = get_db_session()
    session = Session()

    stmt = select(orm.Host)
    result = session.execute(stmt)

    print(result)
    return flask.Response(status=200)
