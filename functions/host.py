"""Module containing function handlers for host requests."""

import flask
from sqlalchemy import select
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


def handle_create_host(request):
    data = request.get_json(silent=True)
    result = parse(data, HostParser)
    if not result.success:
        return f"Failed: {','.join(result.errors)}", 405

    # TODO: proper logs
    if result.warnings:
        print(result.warnings)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        session.commit()
        return "Success", 201
