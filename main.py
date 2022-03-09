# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import os

import functions_framework
import sqlalchemy

from sqlalchemy.orm import sessionmaker

from utils import orm


DRIVER_NAME = "postgres+pg8000"
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

CONNECTION_NAME = "kok"
query_string = {"unix_sock": f"/cloudsql/{CONNECTION_NAME}/.s.PGSQL.5432"}


@functions_framework.http
def get_apartment(request):
    """HTTP Cloud Function for getting apartment."""


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
    session.commit()

    return {}, 201


@functions_framework.http
def put_apartment(request):
    """HTTP Cloud Function for updating apartment."""


@functions_framework.http
def delete_apartment(request):
    """HTTP Cloud Function for deleting apartment."""
