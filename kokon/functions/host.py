"""Module containing function handlers for host requests."""

import flask
import marshmallow
from flask import redirect
from sqlalchemy import select, delete, or_
from sqlalchemy.exc import ProgrammingError

from kokon.utils.authologic import start_conversation
from kokon.orm import Host, Language, HostVerificationSession
from kokon.orm.enums import VerificationStatus
from kokon.serializers import HostSchema, HostSchemaFull
from kokon.utils.functions import Request, JSONResponse
from kokon.utils.query import filter_stmt, paginate, sort_stmt


def handle_get_all_hosts(request: Request):
    query_parameter = request.args.get("query", None)
    language_spoken = request.args.get("languageSpoken", None)

    with request.db.acquire() as session:
        stmt = session.query(Host)

        if language_spoken:
            stmt = stmt.filter(
                Host.languages_spoken.any(Language.code2 == language_spoken)
            )

        if query_parameter:
            query_parameter = f"%{query_parameter}%"
            stmt = stmt.where(
                or_(
                    Host.full_name.ilike(query_parameter),
                    Host.phone_number.ilike(query_parameter),
                )
            )

        stmt = filter_stmt(stmt=stmt, request=request, model=Host)
        stmt = sort_stmt(stmt=stmt, request=request, model=Host)

        response = paginate(stmt, request=request, schema=HostSchema)

    return JSONResponse(response, status=200)


def handle_add_host(request: Request):
    host_schema_full = HostSchemaFull()

    data = request.get_json()

    with request.db.acquire() as session:
        response = add_entry_with_post_data(data, host_schema_full, session)

    return JSONResponse(response, status=201)


def handle_registration(request: Request):
    data = request.get_json()

    with request.db.acquire() as session:
        host_schema_full = HostSchemaFull()
        host = host_schema_full.load(data, session=session)
        result = (
            session.query(Host).where(Host.phone_number == data["phoneNumber"]).first()
        )
        if result is None:
            session.add(host)
            session.commit()
            session.refresh(host)
            host = start_host_verification(host, session, request.host_url)
            response = host_schema_full.dump(host)
            return JSONResponse(response, status=201)
        else:
            return redirect("/")  # TODO: set correct redirect address


def start_host_verification(host, session, host_url):
    host_verification = start_verification_session(host, host_url)
    host.verifications.append(host_verification)
    session.add(host_verification)
    session.commit()
    session.refresh(host)
    return host


def start_verification_session(host, host_url):
    host_verification = HostVerificationSession()
    host_verification.state = VerificationStatus.CREATED
    conversation_result = start_conversation(str(host.guid), host_url)
    host_verification.conversation_id = conversation_result["id"]
    host_verification.url = conversation_result["url"]
    host.verifications.append(host_verification)
    return host_verification


def add_entry_with_post_data(data, schema_full, session):
    host = schema_full.load(data, session=session)
    session.add(host)
    session.commit()
    session.refresh(host)
    response = schema_full.dump(host)
    return response


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
