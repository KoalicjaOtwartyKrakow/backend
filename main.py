# pylint: disable=fixme,invalid-name
"""Module containing Google Cloud functions for deployment."""

import os

import flask
import functions_framework
import sqlalchemy


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

    # check required attributes
    if any(
        attr not in request_json
        for attr in ["zip", "address_line", "vacancies_total", "vacancies_free"]
    ):
        return flask.Response(status=400)

    # sql statement
    stmt = sqlalchemy.text("insert into ")

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

    # execute statement
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    # todo: catch more specific exception
    # pylint: disable=broad-except
    except Exception as e:
        return e

    return flask.Response(status=200)
