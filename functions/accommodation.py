"""Module containing function handlers for accommodation requests."""
import json

import flask
import marshmallow

from sqlalchemy import select, delete
from sqlalchemy.exc import ProgrammingError

from utils.db import acquire_db_session
from utils.orm import AccommodationUnit
from utils.serializers import (
    AccommodationUnitSchemaFull,
    UUIDEncoder,
    AccommodationUnitSchema,
)


def handle_add_accommodation(request):
    schema = AccommodationUnitSchema()
    schema_full = AccommodationUnitSchemaFull()

    data = request.get_json(silent=True)

    with acquire_db_session() as session:
        try:
            accommodation = schema.load(data, session=session)
        except marshmallow.ValidationError as e:
            return flask.Response(
                {"validationErrors": e.messages},
                status=422,
                mimetype="application/json",
            )
        session.add(accommodation)
        session.commit()
        session.refresh(accommodation)
        response = schema_full.dumps(accommodation)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_all_accommodations(request):
    with acquire_db_session() as session:
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

    try:
        with acquire_db_session() as session:
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

    try:
        with acquire_db_session() as session:
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

    try:
        with acquire_db_session() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)

            accommodation = result.scalar()
            if accommodation is None:
                return flask.Response("Not found", status=404)

            try:
                accommodation = schema.load(
                    data, session=session, instance=accommodation
                )
            except marshmallow.ValidationError as e:
                return flask.Response(
                    {"validationErrors": e.messages},
                    status=422,
                    mimetype="application/json",
                )

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
