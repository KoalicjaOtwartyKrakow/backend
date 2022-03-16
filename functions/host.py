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
        return flask.Response(response=f"Failed: {','.join(result.errors)}", status=405)

    if result.warnings:
        print(result.warnings)

    Session = get_db_session()
    with Session() as session:
        session.add(result.payload)
        session.commit()
        return flask.Response(response="Success", status=201)

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
