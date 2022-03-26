"""Module containing function handlers for host requests."""
import flask
import marshmallow
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select, delete

from kokon import orm
from kokon.utils.functions import Request, JSONResponse
from kokon.serializers import HostSchema


def handle_get_all_hosts(request: Request):
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

    with request.db.acquire() as s:
        result = s.execute(stmt)
        host_schema = HostSchema()
        response = [host_schema.dump(g) for g in result.scalars()]

    return JSONResponse(response, status=200)


def handle_add_host(request: Request):
    host_schema = HostSchema()

    data = request.get_json()

    with request.db.acquire() as session:
        host = host_schema.load(data, session=session)
        session.add(host)
        session.commit()
        session.refresh(host)
        response = host_schema.dump(host)

    return JSONResponse(response, status=201)


def handle_get_host_by_id(request: Request):
    host_schema = HostSchema()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            response = host_schema.dump(host)
    except ProgrammingError as e:
        # TODO: raise a validation error here, handle in utils/functions.
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {host_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)


def handle_update_host(request: Request):
    host_schema = HostSchema()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    data = request.get_json()

    with request.db.acquire() as session:
        try:
            stmt = select(orm.Host).where(orm.Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            try:
                host = host_schema.load(data, session=session, instance=host)
            except marshmallow.ValidationError as e:
                return flask.Response(
                    {"validationErrors": e.messages},
                    status=422,
                    mimetype="application/json",
                )

            session.add(host)
            session.commit()
            session.refresh(host)
            response = host_schema.dump(host)
        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {id}", status=400
                )
            raise e

    return JSONResponse(response, status=200)


def handle_delete_host(request: Request):
    try:
        id = request.args.get("hostId")
    except KeyError:
        return flask.Response("No host id supplied!", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)

    with request.db.acquire() as session:
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
