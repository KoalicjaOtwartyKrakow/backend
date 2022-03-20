"""Module containing function handlers for guest requests."""
import json

import flask
import marshmallow

from sqlalchemy import exc, select

from utils.db import get_engine, get_db_session
from utils.orm import Guest
from utils import orm

from utils.serializers import GuestSchema, GuestSchemaFull, UUIDEncoder

global_pool = get_engine()
"""
Global pool,
see https://github.com/KoalicjaOtwartyKrakow/backend/issues/80 for more info
"""


def handle_get_all_guests(request):
    Session = get_db_session(global_pool)
    with Session() as session:
        stmt = select(Guest)
        result = session.execute(stmt)
        guest_schema_full = GuestSchemaFull()
        response = json.dumps(
            [guest_schema_full.dump(g) for g in result.scalars()], cls=UUIDEncoder
        )
    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_add_guest(request):
    guest_schema = GuestSchema()
    guest_schema_full = GuestSchemaFull()

    data = request.get_json()

    Session = get_db_session(global_pool)
    with Session() as session:
        try:
            guest = guest_schema.load(data, session=session)
        except marshmallow.ValidationError as e:
            return flask.Response(
                {"validationErrors": e.messages},
                status=422,
                mimetype="application/json",
            )
        session.add(guest)
        session.commit()
        session.refresh(guest)
        response = guest_schema_full.dumps(guest)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_guest_by_id(request):
    guest_schema_full = GuestSchemaFull()

    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    Session = get_db_session(global_pool)

    try:
        with Session() as session:
            stmt = select(orm.Guest).where(orm.Guest.guid == guest_id)
            result = session.execute(stmt)

            guest = result.scalar()
            if guest is None:
                return flask.Response("Not found", status=404)

            response = guest_schema_full.dumps(guest)
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_delete_guest(request):
    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    Session = get_db_session(global_pool)
    try:
        with Session() as session:
            result1 = (
                session.query(Guest)
                .filter(Guest.guid == guest_id)
                .delete(synchronize_session=False)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return flask.Response(response=f"Guest with id = {guest_id} deleted", status=204)


def handle_update_guest(request):
    guest_schema = GuestSchema()
    guest_schema_full = GuestSchemaFull()

    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    data = request.get_json()

    Session = get_db_session(global_pool)
    try:
        with Session() as session:
            stmt = select(orm.Guest).where(orm.Guest.guid == guest_id)
            result = session.execute(stmt)

            guest = result.scalar()
            if guest is None:
                return flask.Response("Not found", status=404)

            try:
                guest = guest_schema.load(data, session=session, instance=guest)
            except marshmallow.ValidationError as e:
                return flask.Response(
                    {"validationErrors": e.messages},
                    status=422,
                    mimetype="application/json",
                )

            session.add(guest)
            session.commit()
            session.refresh(guest)
            response = guest_schema_full.dumps(guest)
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")
