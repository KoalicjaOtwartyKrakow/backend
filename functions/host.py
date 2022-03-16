"""Module containing function handlers for host requests."""

import flask
from sqlalchemy import select
from utils.db import get_db_session
from utils import orm


def handle_get_all_hosts(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Host)
        result = session.execute(stmt)
        response = [host.to_json() for host in result.scalars()]

    return flask.Response(response=response, status=200)


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
            response = [host.to_json() for host in result.scalars()]
            if len(response) == 0:
                return flask.Response(
                    response=f"Host with status = {status_val} not found", status=404
                )

            return flask.Response(response=response, status=200)

        except TypeError as e:
            return flask.Response(response=f"Received invalid status: {e}", status=405)
