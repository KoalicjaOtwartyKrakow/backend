# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import functions_framework

from sqlalchemy.orm import sessionmaker

from utils import orm, db


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
    engine = db.get_engine()
    session = sessionmaker(bind=engine)
    session.add(apartment)
    session.commit()

    return {}, 201


@functions_framework.http
def put_apartment(request):
    """HTTP Cloud Function for updating apartment."""


@functions_framework.http
def delete_apartment(request):
    """HTTP Cloud Function for deleting apartment."""
