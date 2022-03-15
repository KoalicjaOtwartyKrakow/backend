"""Module containing function handlers for host requests."""

import flask
from sqlalchemy import select, delete
from utils.db import get_db_session
from utils import orm


def handle_get_all_hosts(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Host)
        result = session.execute(stmt)
        response = [host.to_json() for host in result.scalars()]

    return flask.Response(response=response, status=200)


def handle_delete_host(request):
    id = request.args.get("hostId")
    if id is None or not id.isdigit():
        return flask.Response(response=f"Received invalid hostId: {id}", status=400)

    Session = get_db_session()
    with Session() as session:
        try:
            stmt = delete(orm.Host).where(orm.Host.id == int(id))
            res = session.execute(stmt)
            if res.rowcount == 0:
                return flask.Response(
                    response=f"Host with id = {id} not found", status=404
                )
            session.commit()
            return flask.Response(response=f"Host with id = {id} deleted", status=200)

        except TypeError as e:
            return flask.Response(response=f"Received invalid hostId: {e}", status=400)
