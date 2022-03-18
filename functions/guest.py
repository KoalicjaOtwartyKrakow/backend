"""Module containing function handlers for guest requests."""
import json

import flask

from sqlalchemy import exc, select
from sqlalchemy.exc import SQLAlchemyError

from utils.db import get_engine, get_db_session
from utils.orm import Guest, new_alchemy_encoder
from utils import orm, mapper
from utils.payload_parser import parse, GuestParserCreate

# Global pool, see
# https://github.com/KoalicjaOtwartyKrakow/backend/issues/80 for more info
global_pool = get_engine()


def handle_get_all_guests(request):
    Session = get_db_session(global_pool)
    with Session() as session:
        stmt = select(Guest)
        result = session.execute(stmt)
        response = json.dumps(
            list(result.scalars()), cls=new_alchemy_encoder(Guest), check_circular=False
        )
    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_add_guest(request):
    data = request.get_json()
    result = parse(data, GuestParserCreate)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    guest = result.payload

    Session = get_db_session(global_pool)
    with Session() as session:
        session.add(guest)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status=400)
        session.refresh(guest)
        response = get_guest_json(guest)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_guest_by_id(request):
    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    Session = get_db_session(global_pool)

    try:
        with Session() as session:
            stmt = select(orm.Guest).where(orm.Guest.guid == guest_id)
            result = session.execute(stmt)
            maybe_result = result.scalar()

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = get_guest_json(maybe_result)
    except SQLAlchemyError:
        return flask.Response("Invaild id format, uuid expected", status=400)

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
    except exc.SQLAlchemyError as e:
        return flask.Response(f"delete_guest unsuccessful e: {e}", status=400)

    return flask.Response(status=200)


def handle_update_guest(request):
    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    request_json = request.get_json()
    mapped_data = mapper.map_guest_from_front_to_db(request_json)

    Session = get_db_session(global_pool)
    try:
        with Session() as session:
            result1 = (
                session.query(Guest).filter(Guest.guid == guest_id).update(mapped_data)
            )
            result2 = session.commit()
            print(f"result1: {result1} \n result2:{result2}")

            stmt = select(orm.Guest).where(orm.Guest.guid == guest_id)
            result = session.execute(stmt)
            maybe_result = result.scalar()

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = get_guest_json(maybe_result)
    except exc.SQLAlchemyError as e:
        return flask.Response(f"update_guest unsuccessful e: {e}", status=400)

    return flask.Response(response=response, status=200, mimetype="application/json")


def get_guest_json(obj):
    return json.dumps(
        obj,
        cls=new_alchemy_encoder(Guest),
        check_circular=False,
    )
