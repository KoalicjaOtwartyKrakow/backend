"""Module containing function handlers for accommodation requests."""

import flask

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

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


def handle_delete_accommodation(request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    Session = get_db_session()

    try:
        with Session() as session:
            stmt = (
                delete(AccommodationUnit)
                .where(AccommodationUnit.guid == accommodation_id)
                .execution_options(synchronize_session="fetch")
            )
            result = session.execute(stmt)
    except SQLAlchemyError:
        return flask.Response("Invalid accommodation id", status=400)

    if result.rowcount:
        return "OK"
    else:
        return flask.Response("Not found", status=404)


def handle_update_accommodation(request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    Session = get_db_session()

    with Session() as session:
        stmt = update(AccommodationUnit).where(
            AccommodationUnit.guid == accommodation_id
        )
        session.execute(stmt)
