"""Module containing function handlers for host requests."""

import flask
from sqlalchemy import select, exc, update
from utils.db import get_db_session
from utils import orm
from utils.payload_parser import parse, HostParser


def handle_get_all_hosts(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Host)
        result = session.execute(stmt)
        response = [host.to_json() for host in result.scalars()]

    return flask.Response(response=response, status=200)


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
