"""Module containing function handlers for accommodation requests."""

import flask

from sqlalchemy import select

from utils.db import get_db_session
from utils.orm import AccommodationUnit
from utils.payload_parser import parse, AccommodationParser


def handle_add_accommodation(request):
    data = request.get_json(silent=True)
    result = parse(data, AccommodationParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        session.commit()
        return flask.Response(response="Success", status=201)


def handle_get_all_accommodations(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(AccommodationUnit)
        result = session.execute(stmt)

    response = [accommodation.to_json() for accommodation in result.scalars()]

    return flask.Response(response=response, status=200)
