"""Module containing function handlers for accommodation requests."""
import json

import flask

from sqlalchemy import select, delete
from sqlalchemy.exc import ProgrammingError

from utils.db import get_engine, get_db_session
from utils.orm import AccommodationUnit
from utils.serializers import (
    AccommodationUnitSchemaFull,
    UUIDEncoder,
    AccommodationUnitSchema,
)

global_pool = get_engine()
"""
Global pool,
see https://github.com/KoalicjaOtwartyKrakow/backend/issues/80 for more info
"""


def handle_add_accommodation(request):
    schema = AccommodationUnitSchema()
    schema_full = AccommodationUnitSchemaFull()

    data = request.get_json(silent=True)

    Session = get_db_session(global_pool)
    with Session() as session:
        accommodation = schema.load(data, session=session)
        session.add(accommodation)
        session.commit()
        session.refresh(accommodation)
        response = schema_full.dumps(accommodation)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_all_accommodations(request):
    Session = get_db_session(global_pool)
    with Session() as session:
        stmt = select(AccommodationUnit).order_by(
            AccommodationUnit.vacancies_free.desc()
        )
        result = session.execute(stmt)
        schema_full = AccommodationUnitSchemaFull()
        response = json.dumps(
            [schema_full.dump(a) for a in result.scalars()], cls=UUIDEncoder
        )

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_delete_accommodation(request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    Session = get_db_session(global_pool)

    try:
        with Session() as session:
            stmt = (
                delete(AccommodationUnit)
                .where(AccommodationUnit.guid == accommodation_id)
                .execution_options(synchronize_session="fetch")
            )
            result = session.execute(stmt)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    if result.rowcount:
        return flask.Response(
            response=f"Accommodation with id = {accommodation_id} deleted", status=204
        )
    else:
        return flask.Response("Not found", status=404)


def handle_get_accommodation_by_id(request):
    schema_full = AccommodationUnitSchemaFull()

    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    Session = get_db_session(global_pool)

    try:
        with Session() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)

            accommodation = result.scalar()
            if accommodation is None:
                return flask.Response("Not found", status=404)

            response = schema_full.dumps(accommodation)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_accommodation(request):
    schema = AccommodationUnitSchema()
    schema_full = AccommodationUnitSchemaFull()

    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    data = request.get_json()

    Session = get_db_session(global_pool)
    try:
        with Session() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)

            accommodation = result.scalar()
            if accommodation is None:
                return flask.Response("Not found", status=404)

            accommodation = schema.load(data, session=session, instance=accommodation)

            session.add(accommodation)
            session.commit()
            session.refresh(accommodation)
            response = schema_full.dumps(accommodation)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")
