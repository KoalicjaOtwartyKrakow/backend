"""Module containing function handlers for accommodation requests."""
import flask
import marshmallow

from sqlalchemy import select, delete
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import joinedload

from kokon.orm import AccommodationUnit, Host
from kokon.serializers import AccommodationUnitSchema, AccommodationUnitSchemaFull
from kokon.utils.functions import JSONResponse, Request
from kokon.utils.pagination import paginate


def accommodation_function(request: Request):
    if request.method == "GET":
        if "accommodationId" in request.args:
            return handle_get_accommodation_by_id(request)
        else:
            return handle_get_all_accommodations(request)
    elif request.method == "PUT":
        return handle_add_accommodation(request)
    elif request.method == "DELETE":
        return handle_delete_accommodation(request)
    elif request.method == "POST":
        return handle_update_accommodation(request)


def handle_add_accommodation(request: Request):
    schema = AccommodationUnitSchema()
    schema_full = AccommodationUnitSchemaFull()

    data = request.get_json(silent=True)

    with request.db.acquire() as session:
        accommodation = schema.load(data, session=session)
        session.add(accommodation)
        session.commit()
        session.refresh(accommodation)
        response = schema_full.dump(accommodation)

    return JSONResponse(response, status=201)


def handle_get_all_accommodations(request: Request):
    with request.db.acquire() as session:
        stmt = (
            session.query(AccommodationUnit)
            .order_by(AccommodationUnit.vacancies_free.desc())
            .options(
                joinedload(AccommodationUnit.host).subqueryload(Host.languages_spoken)
            )
        )

        response = paginate(stmt, request=request, schema=AccommodationUnitSchemaFull)

    return JSONResponse(response, status=200)


def handle_delete_accommodation(request: Request):
    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            stmt = (
                delete(AccommodationUnit)
                .where(AccommodationUnit.guid == accommodation_id)
                .execution_options(synchronize_session="fetch")
            )
            result = session.execute(stmt)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    if result.rowcount:
        return flask.Response(
            response=f"Accommodation with id = {accommodation_id} deleted", status=204
        )
    else:
        return flask.Response("Not found", status=404)


def handle_get_accommodation_by_id(request: Request):
    schema_full = AccommodationUnitSchemaFull()

    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    try:
        with request.db.acquire() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)

            accommodation = result.scalar()
            if accommodation is None:
                return flask.Response("Not found", status=404)

            response = schema_full.dump(accommodation)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)


def handle_update_accommodation(request: Request):
    schema = AccommodationUnitSchema()
    schema_full = AccommodationUnitSchemaFull()

    try:
        accommodation_id = request.args["accommodationId"]
    except KeyError:
        return flask.Response("No accommodation id supplied!", status=400)

    data = request.get_json()

    try:
        with request.db.acquire() as session:
            stmt = select(AccommodationUnit).where(
                AccommodationUnit.guid == accommodation_id
            )
            result = session.execute(stmt)

            accommodation = result.scalar()
            if accommodation is None:
                return flask.Response("Not found", status=404)

            try:
                accommodation = schema.load(
                    data, session=session, instance=accommodation
                )
            except marshmallow.ValidationError as e:
                return JSONResponse(
                    {"validationErrors": e.messages},
                    status=422,
                )

            session.add(accommodation)
            session.commit()
            session.refresh(accommodation)
            response = schema_full.dump(accommodation)
    except ProgrammingError as e:
        if "invalid input syntax for type uuid" in str(e):
            return flask.Response(
                f"Invaild id format, uuid expected, got {accommodation_id}", status=400
            )
        raise e

    return JSONResponse(response, status=200)
