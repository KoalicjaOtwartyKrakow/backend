"""Module containing function handlers for teammember requests."""
import json

import flask

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from utils.db import get_db_session
from utils.orm import Teammember, new_alchemy_encoder
from utils.payload_parser import parse, TeammemberParser


def handle_add_teammember(request):
    data = request.get_json(silent=True)
    result = parse(data, TeammemberParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        session.commit()
        return flask.Response(response=[], status=201)


def handle_get_all_teammembers(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(Teammember)
        result = session.execute(stmt)

        response = json.dumps(
            list(result.scalars()),
            cls=new_alchemy_encoder(Teammember),
            check_circular=False,
        )

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_delete_teammember(request):
    try:
        teammember_id = request.args["teammemberId"]
    except KeyError:
        return flask.Response("No teammember id supplied!", status=400)

    Session = get_db_session()

    try:
        with Session() as session:
            stmt = (
                delete(Teammember)
                .where(Teammember.guid == teammember_id)
                .execution_options(synchronize_session="fetch")
            )
            result = session.execute(stmt)
    except SQLAlchemyError:
        return flask.Response("Invalid teammember id", status=400)

    if result.rowcount:
        return flask.Response([], status=200)
    else:
        return flask.Response("Not found", status=404)


def handle_get_teammember_by_id(request):
    try:
        teammember_id = request.args["teammemberId"]
    except KeyError:
        return flask.Response("No teammember id supplied!", status=400)

    Session = get_db_session()

    try:
        with Session() as session:
            stmt = select(Teammember).where(Teammember.guid == teammember_id)
            result = session.execute(stmt)
            maybe_result = list(result.scalars())

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = json.dumps(
                maybe_result[0],
                cls=new_alchemy_encoder(Teammember),
                check_circular=False,
            )
    except SQLAlchemyError:
        return flask.Response("Invaild id format, uuid expected", status=400)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_teammember(request):
    try:
        teammember_id = request.args["teammemberId"]
    except KeyError:
        return flask.Response("No teammember id supplied!", status=400)

    data = request.get_json(silent=True)
    result = parse(data, TeammemberParser)

    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    Session = get_db_session()
    try:
        with Session() as session:
            stmt = (
                update(Teammember)
                .where(Teammember.guid == teammember_id)
                .values(**result.payload)
            )
            result = session.execute(stmt)
    except SQLAlchemyError:
        return flask.Response("Could not update object, invalid input", status=405)

    if result.rowcount:
        return flask.Response([], status=200)
    else:
        return flask.Response("Not found", status=404)
