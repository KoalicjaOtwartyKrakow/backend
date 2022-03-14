"""Module containing function handlers for guest requests."""

import flask
from sqlalchemy import select
from utils.db import get_db_session
from utils import orm


def handle_get_all_guests(request):
    Session = get_db_session()
    with Session() as session:
        stmt = select(orm.Guest)
        result = session.execute(stmt)
        response = [guest.to_json() for guest in result.scalars()]

    return flask.Response(response=response, status=200)
