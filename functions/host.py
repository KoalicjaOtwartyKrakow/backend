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
