"""Module containing function handlers for accommodation requests."""
import json

import flask

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from utils.db import get_db_session
from utils.orm import AccommodationUnit, new_alchemy_encoder
from utils.payload_parser import parse, AccommodationParser
from utils import mapper


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
        return flask.Response(response=[], status=201)


def handle_get_all_accommodations(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(AccommodationUnit).order_by(
            AccommodationUnit.vacancies_free.desc()
        )
        result = session.execute(stmt)

        response = json.dumps(
            list(result.scalars()),
            cls=new_alchemy_encoder(AccommodationUnit),
            check_circular=False,
        )

    return flask.Response(response=response, status=200, mimetype="application/json")


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
        return flask.Response([], status=200)
    else:
        return flask.Response("Not found", status=404)


def handle_get_accommodation_by_id(request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    Session = get_db_session()

    try:
        with Session() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)
            maybe_result = list(result.scalars())

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = json.dumps(
                maybe_result[0],
                cls=new_alchemy_encoder(AccommodationUnit),
                check_circular=False,
            )
    except SQLAlchemyError:
        return flask.Response("Invaild id format, uuid expected", status=400)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_accommodation(request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    request_json = request.get_json(silent=True)
    mapped_data = mapper.map_guest_from_front_to_db(request_json)
    Session = get_db_session()

    try:
        with Session() as session:
            result = (
                session.query(AccommodationUnit)
                .filter(AccommodationUnit.guid == accommodation_id)
                .update(mapped_data)
            )
            session.commit()
    except SQLAlchemyError:
        return flask.Response("Could not update object, invalid input", status=405)

    if result.rowcount:
        return flask.Response([], status=200)
    else:
        return flask.Response("Not found", status=404)
