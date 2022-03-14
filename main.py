# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import flask
import functions_framework

import json

from sqlalchemy import exc, select
from utils.db import get_db_session

from utils import orm
from functions import handle_create_host
from functions import accommodation


@functions_framework.http
def add_accommodation(request):
    """HTTP Cloud Function for posting new accommodation units."""
    return accommodation.handle_add_accommodation(request)


@functions_framework.http
def get_all_accommodations(request):
    """HTTP Cloud Function for getting all available accommodation units."""
    return accommodation.handle_get_all_accommodations(request)


@functions_framework.http
def create_host(request):
    return handle_create_host(request)


# #TODO: move to guest.py file
@functions_framework.http
def get_all_guests(request):
    """HTTP Cloud Function for getting all guests."""
    Session = get_db_session()
    session = Session()
    # #TODO: It might not read from db
    stmt = select(orm.Guest)
    result = session.execute(stmt)

    for row in result:
        print(row)
    print(result)
    jsonResults = json.dumps([dict(r) for r in result])
    print(jsonResults)
    # #TODO: Nothing returned in response
    return flask.Response(response=f"response: {result}", status=200)


@functions_framework.http
def add_guest(request):
    """HTTP Cloud Function for posting new guests."""
    # parse request
    request_json = request.get_json()

    # create Guest object from json
    try:
        guest = orm.Guest(**request_json)
    except TypeError as e:
        return flask.Response(
            response=f"Received invalid parameter(s) for guest: {e}", status=405
        )
    Session = get_db_session()
    with Session() as session:
        session.add(guest)
        # db transaction
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status=400)

        return flask.Response(status=201)
