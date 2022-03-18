"""Module containing function handlers for host requests."""
import json

import flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, exc, delete
from utils.db import get_engine, get_db_session
from utils import orm
from utils.orm import new_alchemy_encoder, Host
from utils.payload_parser import parse, HostParser

# Global pool, see https://github.com/KoalicjaOtwartyKrakow/backend/issues/80 for more info
global_pool = get_engine()

def handle_get_all_hosts(request):
    Session = get_db_session(global_pool)
    with Session() as session:
        stmt = select(orm.Host)
        result = session.execute(stmt)
        print(result.scalars())
        response = json.dumps(
            list(result.scalars()), cls=new_alchemy_encoder(Host), check_circular=False
        )
        print(response)

    return flask.Response(response=response, status=200, mimetype="application/json")


def handle_add_host(request):
    data = request.get_json(silent=True)
    result = parse(data, HostParser)
    if not result.success:
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    Session = get_db_session(global_pool)
    stmt1 = select(orm.Language).where(
        orm.Language.code2.in_(result.payload.languages_spoken)
    )
    with Session() as session:
        langs = list(session.execute(stmt1).scalars())
        result.payload.languages_spoken = langs
        session.add(result.payload)
        session.commit()
        return flask.Response(response="Success", status=201)


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
            maybe_result = list(result.scalars())

            if not maybe_result:
                return flask.Response("Not found", status=404)

            response = json.dumps(
                maybe_result[0], cls=new_alchemy_encoder(Host), check_circular=False
            )
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
    Session = get_db_session(global_pool)

    with Session() as session:
        try:
            result = session.execute(stmt)

            response = json.dumps(
                list(result.scalars()),
                cls=new_alchemy_encoder(Host),
                check_circular=False,
            )
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

    stmt1 = select(orm.Host).where(orm.Host.guid == id)
    stmt2 = select(orm.Language).where(
        orm.Language.code2.in_(result.payload.languages_spoken)
    )

    Session = get_db_session(global_pool)
    with Session() as session:
        try:
            res = session.execute(stmt1).scalar()
            if not res:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )
            langs = list(session.execute(stmt2).scalars())

            res.full_name = result.payload.full_name
            res.email = result.payload.email
            res.phone_number = result.payload.phone_number
            res.call_after = result.payload.call_after
            res.call_before = result.payload.call_before
            res.comments = result.payload.comments
            res.languages_spoken = langs
            if result.payload.status:
                res.status = result.payload.status
            session.add(res)
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
            return flask.Response(response=f"Host with id = {id} deleted", status=200)

        except SQLAlchemyError:
            return flask.Response(response=f"Received invalid hostId: {id}", status=400)
