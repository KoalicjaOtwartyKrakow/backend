"""Module containing function handlers for host requests."""
import json

import flask
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select, delete

from utils.db import acquire_db_session
from utils import orm

from utils.serializers import HostSchema, UUIDEncoder


def handle_get_all_hosts(request):
    status_parameter = request.args.get("status", None)
    if status_parameter:
        try:
            status_parameter = orm.VerificationStatus(status_parameter)
        except ValueError:
            print(
                f"Could not understand status={status_parameter}. Filtering disabled."
            )
            return flask.Response(
                response=f"Received invalid status: {status_parameter}", status=400
            )

    stmt = select(orm.Host)
    if status_parameter:
        print(f"Filtering by status={status_parameter}")
        stmt = stmt.where(orm.Host.status == status_parameter)

    with acquire_db_session() as s:
        result = s.execute(stmt)
        host_schema = HostSchema()
        response = json.dumps(
            [host_schema.dump(g) for g in result.scalars()], cls=UUIDEncoder
        )

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_add_host(request):
    host_schema = HostSchema()

    data = request.get_json()

    with acquire_db_session() as session:
        host = host_schema.load(data, session=session)
        session.add(host)
        session.commit()
        session.refresh(host)
        response = host_schema.dumps(host)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_host_by_id(request):
    host_schema = HostSchema()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    try:
        with acquire_db_session() as session:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            response = host_schema.dumps(host)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {host_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_host(request):
    host_schema = HostSchema()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    data = request.get_json()

    with acquire_db_session() as session:
        try:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            host = host_schema.load(data, session=session, instance=host)

            session.add(host)
            session.commit()
            session.refresh(host)
            response = host_schema.dumps(host)
        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {id}", status=400
                )
            raise e

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_delete_host(request):
    try:
        id = request.args.get("hostId")
    except KeyError:
        return flask.Response("No host id supplied!", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)

    with acquire_db_session() as session:
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
            return flask.Response(response=f"Host with id = {id} deleted", status=204)

        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {id}", status=400
                )
            raise e
