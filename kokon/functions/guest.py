"""Module containing function handlers for guest requests."""
import flask
from sqlalchemy import exc, select

from kokon.orm import Guest
from kokon.serializers import GuestSchema
from kokon.utils.functions import Request, JSONResponse


def handle_get_all_guests(request: Request):
    with request.db.acquire() as session:
        result = session.query(Guest).all()
        response = GuestSchema().dump(result, many=True)

    return JSONResponse(response, status=200)


def handle_add_guest(request: Request):
    schema = GuestSchema()

    data = request.get_json()

    with request.db.acquire() as session:
        guest = schema.load(data, session=session)
        guest.updated_by_id = request.user.guid
        session.add(guest)
        session.commit()
        session.refresh(guest)
        response = schema.dump(guest)

    return JSONResponse(response, status=201)


def handle_get_guest_by_id(request: Request):
    schema = GuestSchema()

    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            stmt = select(Guest).where(Guest.guid == guest_id)
            result = session.execute(stmt)

            guest = result.scalar()
            if guest is None:
                return flask.Response("Not found", status=404)

            response = schema.dump(guest)
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)


def handle_delete_guest(request: Request):
    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            guest = session.query(Guest).filter(Guest.guid == guest_id).one()

            # record last editor
            guest.updated_by_id = request.user.guid
            session.commit()

            session.delete(guest)
            session.commit()
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return flask.Response(response=f"Guest with id = {guest_id} deleted", status=204)


def handle_update_guest(request: Request):
    schema = GuestSchema()

    try:
        guest_id = request.args["guestId"]
    except KeyError:
        return flask.Response("No guest id supplied!", status=400)

    data = request.get_json()

    try:
        with request.db.acquire() as session:
            stmt = select(Guest).where(Guest.guid == guest_id)
            result = session.execute(stmt)

            guest = result.scalar()
            if guest is None:
                return flask.Response("Not found", status=404)

            guest = schema.load(data, session=session, instance=guest)
            guest.updated_by_id = request.user.guid

            session.commit()
            session.refresh(guest)
            response = schema.dump(guest)
    except exc.ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {guest_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)
