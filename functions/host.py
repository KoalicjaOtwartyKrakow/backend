"""Module containing function handlers for host requests."""
import json

import flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, exc, update, delete
from utils.db import get_db_session
from utils import orm
from utils.orm import AlchemyEncoder
from utils.payload_parser import parse, HostParser


def handle_get_all_hosts(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Host)
        result = session.execute(stmt)

        response = json.dumps(list(result.scalars()), cls=AlchemyEncoder)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_create_host(request):
    data = request.get_json(silent=True)
    result = parse(data, HostParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        session.commit()
        return flask.Response(response="Success", status=201)


def handle_get_host_by_id(request):
    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    Session = get_db_session()

    try:
        with Session() as session:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)
            maybe_result = list(result.scalars())

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = json.dumps(maybe_result[0], cls=AlchemyEncoder)
    except SQLAlchemyError:
        return flask.Response("Invaild id format, uuid expected", status=400)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_get_hosts_by_status(request):
    status_val = request.args.get("status")
    try:
        status_val = orm.Status(status_val)
    except ValueError:
        return flask.Response(
            response=f"Received invalid status: {status_val}", status=400
        )

    stmt = select(orm.Host).where(orm.Host.status == status_val)
    Session = get_db_session()

    with Session() as session:
        try:
            result = session.execute(stmt)

            response = json.dumps(list(result.scalars()), cls=AlchemyEncoder)
        except TypeError as e:
            return flask.Response(response=f"Received invalid status: {e}", status=405)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_host(request):
    try:
        id = request.args.get("hostId")
    except ValueError:
        return flask.Response(response=f"Received invalid hostId: {id}", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)
    data = request.get_json()
    result = parse(data, HostParser)

    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    stmt = (
        update(orm.Host)
        .where(orm.Host.guid == id)
        .values(
            full_name=result.payload.full_name,
            email=result.payload.email,
            phone_number=result.payload.phone_number,
            call_after=result.payload.call_after,
            call_before=result.payload.call_before,
            comments=result.payload.comments,
            # languages_spoken=result.payload.languages_spoken,
            # status=result.payload.status,
        )
    )
    # TODO: Uncomment these ^ fields here when HostParser is fixed
    # parser doesn't parse languages_spoken correctly, and doesn't parse status at all.

    Session = get_db_session()
    with Session() as session:
        try:
            res = session.execute(stmt)
            if res.rowcount == 0:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )

            session.commit()

        except exc.SQLAlchemyError as e:
            return flask.Response(response=f"Transaction error: {e}", status=400)

    return flask.Response(response=f"Updated host with id {id}", status=200)


def handle_delete_host(request):
    try:
        id = request.args.get("hostId")
    except KeyError:
        return flask.Response("No host id supplied!", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)

    Session = get_db_session()
    with Session() as session:
        try:
            stmt = (
                delete(orm.Host)
                .where(orm.Host.guid == id)
                .execution_options(synchronize_session="fetch")
            )
            res = session.execute(stmt)
            if res.rowcount == 0:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )
            session.commit()
            return flask.Response(response=f"Host with id = {id} deleted", status=200)

        except SQLAlchemyError:
            return flask.Response(response=f"Received invalid hostId: {id}", status=400)
