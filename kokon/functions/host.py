"""Module containing function handlers for host requests."""
import flask
import marshmallow
from sqlalchemy import select, delete, or_
from sqlalchemy.exc import ProgrammingError

from kokon.orm import Host, enums
from kokon.serializers import HostSchema, HostSchemaFull
from kokon.utils.functions import Request, JSONResponse
from kokon.utils.pagination import paginate


def handle_get_all_hosts(request: Request):
    status_parameter = request.args.get("status", None)
    query_parameter = request.args.get("query", None)
    if status_parameter:
        try:
            status_parameter = enums.VerificationStatus(status_parameter)
        except ValueError:
            return flask.Response(
                response=f"Received invalid status: {status_parameter}", status=400
            )

    with request.db.acquire() as session:
        stmt = session.query(Host)
        if status_parameter:
            stmt = stmt.where(Host.status == status_parameter)

        if query_parameter:
            query_parameter = f"%{query_parameter}%"
            stmt = stmt.where(
                or_(
                    Host.full_name.ilike(query_parameter),
                    Host.phone_number.ilike(query_parameter),
                )
            )

        response = paginate(stmt, request=request, schema=HostSchema)

    return JSONResponse(response, status=200)


def handle_add_host(request: Request):
    host_schema_full = HostSchemaFull()

    data = request.get_json()

    with request.db.acquire() as session:
        host = host_schema_full.load(data, session=session)
        session.add(host)
        session.commit()
        session.refresh(host)
        response = host_schema_full.dump(host)

    return JSONResponse(response, status=201)


def handle_get_host_by_id(request: Request):
    host_schema_full = HostSchemaFull()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            stmt = select(Host).where(Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            response = host_schema_full.dump(host)
    except ProgrammingError as e:
        # TODO: raise a validation error here, handle in utils/functions.
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {host_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)


def handle_update_host(request: Request):
    host_schema_full = HostSchemaFull()

    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    data = request.get_json()

    with request.db.acquire() as session:
        try:
            stmt = select(Host).where(Host.guid == host_id)
            result = session.execute(stmt)

            host = result.scalar()
            if host is None:
                return flask.Response("Not found", status=404)

            try:
                host = host_schema_full.load(data, session=session, instance=host)
            except marshmallow.ValidationError as e:
                return flask.Response(
                    {"validationErrors": e.messages},
                    status=422,
                    mimetype="application/json",
                )

            session.add(host)
            session.commit()
            session.refresh(host)
            response = host_schema_full.dump(host)
        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {id}", status=400
                )
            raise e

    return JSONResponse(response, status=200)


def handle_delete_host(request: Request):
    try:
        host_id = request.args["hostId"]
    except KeyError:
        return flask.Response("No host id supplied!", status=400)

    with request.db.acquire() as session:
        try:
            stmt = (
                delete(Host)
                .where(Host.guid == host_id)
                .execution_options(synchronize_session="fetch")
            )
            res = session.execute(stmt)
            if res.rowcount == 0:
                return flask.Response(
                    response=f"Host with id = {host_id} not found", status=404
                )
            session.commit()
            return flask.Response(
                response=f"Host with id = {host_id} deleted", status=204
            )

        except ProgrammingError as e:
            if "invalid input syntax for type uuid" in str(e):
                return flask.Response(
                    f"Invaild id format, uuid expected, got {host_id}", status=400
                )
            raise e
