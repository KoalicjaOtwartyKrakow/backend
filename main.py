# pylint: disable=fixme,invalid-name,no-member
"""Module containing Google Cloud functions for deployment."""

import os

import flask
import functions_framework
import sqlalchemy

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from utils import orm


DRIVER_NAME = "postgres+pg8000"
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

CONNECTION_NAME = "kok"
query_string = {"unix_sock": f"/cloudsql/{CONNECTION_NAME}/.s.PGSQL.5432"}

APARTMENTS_TABLE_NAME = ...


@functions_framework.http
def post_apartment(request):
    """HTTP Cloud Function for posting new apartments."""
    # parse request
    request_json = request.get_json()

    # create Apartment object from json
    try:
        apartment = orm.Apartment(**request_json)
    except TypeError as e:
        return (f"Received invalid parameter(s) for apartment: {e}", 400)

    # db connection
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername=DRIVER_NAME,
            username=db_user,
            password=db_password,
            database=db_name,
            query=query_string,
        )
    )
    session = sessionmaker(bind=db)
    session.add(apartment)

    # db transaction
    try:
        session.commit()
    except exc.SQLAlchemyError as e:
        return (f"Transaction error: {e}", 400)

    return flask.Response(status=200)
