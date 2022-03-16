# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import flask
import functions_framework

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
    stmt = select(orm.Guest)
    # stmt = select(orm.Guest).where(orm.Guest.id == 4)
    result = session.execute(stmt)
    response = [guest.to_json() for guest in result.scalars()]
    return flask.Response(response=response, status=200)


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


@functions_framework.http
def get_guest_by_id(request):
    print(request.__dict__)
    print(f"Path: {request.path}")
    value = request.path.split("/")
    print(f"Path+split: {value}")
    guest_id = value[len(value) - 1]
    print(f"Path+split+value: {guest_id}")
    Session = get_db_session()
    session = Session()
    stmt = select(orm.Guest).where(orm.Guest.guid == guest_id)
    print(stmt)
    result = session.execute(stmt)
    response = [guest.to_json() for guest in result.scalars()]
    return flask.Response(response=response, status=200)


# TODO: GET method also allows to remove data
@functions_framework.http
def delete_guest(request):
    print(request.__dict__)
    print(f"Path: {request.path}")
    value = request.path.split("/")
    print(f"Path+split: {value}")
    guest_id = value[len(value) - 1]
    print(f"Path+split+value: {guest_id}")
    print(orm.Guest.guid)
    Session = get_db_session()
    try:
        with Session() as session:
            result1 = (
                session.query(orm.Guest)
                .filter(orm.Guest.guid == guest_id)
                .delete(synchronize_session=False)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")
    except exc.SQLAlchemyError:
        return flask.Response("Invalid accommodation id", status=400)

    return flask.Response(status=200)


def update_guest(request):
    print(request.__dict__)
    print(f"Path: {request.path}")
    value = request.path.split("/")
    print(f"Path+split: {value}")
    guest_id = value[len(value) - 1]
    print(f"Path+split+value: {guest_id}")
    print(orm.Guest.guid)

    request_json = request.get_json()
    print(request_json)
    Session = get_db_session()
    try:
        with Session() as session:
            result1 = (
                session.query(orm.Guest)
                .filter(orm.Guest.guid == guest_id)
                .update(request_json)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")
    except exc.SQLAlchemyError:
        return flask.Response("Invalid accommodation id", status=400)

    return flask.Response(status=200)
