"""Module containing function handlers for host requests."""
import json

import flask
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select, update, delete
from utils.db import get_engine, get_db_session
from utils import orm, mapper
from utils.orm import new_alchemy_encoder, Host
from utils.payload_parser import parse, HostParser

# Global pool,
# see https://github.com/KoalicjaOtwartyKrakow/backend/issues/80 for more info
global_pool = get_engine()


def handle_get_all_hosts(request):
    status_parameter = request.args.get("status", None)
    if status_parameter:
        try:
            status_parameter = orm.Status(status_parameter)
        except ValueError:
            print(
                f"Could not understand status={status_parameter}. Filtering disabled."
            )
            return flask.Response(response=f"Received invalid status: {status_parameter}", status=400)

    stmt = select(orm.Host)
    if status_parameter:
        print(f"Filtering by status={status_parameter}")
        stmt = stmt.where(orm.Host.status == status_parameter)

    session = get_db_session(global_pool)
    with session() as s:
        try:
            result = s.execute(stmt)
            response = get_host_json(list(result.scalars()))
            return flask.Response(
                response=response, status=200, mimetype="application/json"
            )
        except TypeError as e:
            return flask.Response(response=f"Received invalid status: {e}", status=400)


def handle_add_host(request):
    data = request.get_json(silent=True)
    result = parse(data, HostParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    host = result.payload

    Session = get_db_session(global_pool)
    stmt1 = select(orm.Language).where(
        orm.Language.code2.in_(result.payload.languages_spoken)
    )
    with Session() as session:
        langs = list(session.execute(stmt1).scalars())
        host.languages_spoken = langs
        session.add(host)
        session.commit()
        session.refresh(host)
        response = get_host_json(host)

    return flask.Response(response=response, status=201, mimetype="application/json")


def handle_get_host_by_id(request):
    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    Session = get_db_session(global_pool)

    try:
        with Session() as session:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            response = get_host_json(host)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {host_id}", status=400
            )
        raise e

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_update_host(request):
    try:
        id = request.args.get("hostId")
    except ValueError:
        return flask.Response(response=f"Received invalid hostId: {id}", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)

    data = request.get_json()
    result = mapper.map_host_from_front_to_db(data)

    languages_spoken = None
    if "languages_spoken" in result:
        languages_spoken = [lang["code2"] for lang in result["languages_spoken"]]
        del result["languages_spoken"]

    stmt1 = update(orm.Host).where(orm.Host.guid == id).values(**result)
    stmt2 = select(orm.Language).where(orm.Language.code2.in_(languages_spoken or []))

    Session = get_db_session(global_pool)
    with Session() as session:
        try:
            res = session.execute(stmt1)
            if res.rowcount == 0:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )

            stmt = select(orm.Host).where(orm.Host.guid == id)
            host = session.execute(stmt).scalar()
            if languages_spoken:
                langs = list(session.execute(stmt2).scalars())
                host.languages_spoken = langs
                session.add(host)

            session.commit()
            session.refresh(host)
            response = get_host_json(host)
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

    Session = get_db_session(global_pool)
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
            return flask.Response(response=f"Host with id = {id} deleted", status=204)

        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {id}", status=400
                )
            raise e


def get_host_json(obj):
    return json.dumps(
        obj,
        cls=new_alchemy_encoder(Host),
        check_circular=False,
    )
