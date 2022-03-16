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


def handle_get_host_by_id(request):
    try:
        id = request.args.get("hostId")
    except ValueError:
        return flask.Response(response=f"Received invalid hostId: {id}", status=400)
    if id is None:
        return flask.Response(response="Received no hostId", status=400)

    Session = get_db_session()
    with Session() as session:
        try:
            stmt = select(orm.Host).where(orm.Host.guid == id)
            res = session.execute(stmt)
            response = [host.to_json() for host in res.scalars()]
            if len(response) == 0:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )
            return flask.Response(response=response, status=200)
        except TypeError as e:
            return flask.Response(response=f"Received invalid hostId: {e}", status=400)
