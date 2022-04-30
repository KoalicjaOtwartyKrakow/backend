"""Module containing function handlers for accommodation requests."""
import flask
import marshmallow

from sqlalchemy import select, delete, func
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import joinedload

from kokon.orm import AccommodationUnit, Host, HostVerificationSession
from kokon.serializers import (
    AccommodationUnitSchema,
    AccommodationUnitSchemaFull,
    SelfCreateAccommodationUnitSchema,
)
from kokon.utils.functions import JSONResponse, Request
from kokon.utils.query import filter_stmt, paginate, sort_stmt


def accommodation_function(request: Request):
    if request.method == "GET":
        if "accommodationId" in request.args:
            return handle_get_accommodation_by_id(request)
        else:
            return handle_get_all_accommodations(request)
    elif request.method == "POST":
        return handle_add_accommodation(request)
    elif request.method == "DELETE":
        return handle_delete_accommodation(request)
    elif request.method == "PUT":
        return handle_update_accommodation(request)
    else:
        return JSONResponse({"message": "Invalid method"}, status=405)


def public_accommodation_function(request: Request):
    if request.method == "POST":
        return handle_public_add_accommodation(request)
    else:
        return JSONResponse({"message": "Invalid method"}, status=405)


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

        stmt = filter_stmt(stmt, request=request, model=AccommodationUnit)
        stmt = sort_stmt(stmt, request=request, model=AccommodationUnit)

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


def handle_public_add_accommodation(request: Request):
    try:
        conversation_id = request.args["conversationId"]
    except KeyError:
        return flask.Response("No conversation id supplied!", status=400)

    schema = SelfCreateAccommodationUnitSchema(many=True)
    schema_full = AccommodationUnitSchemaFull(many=True)

    data = request.get_json(silent=True)

    with request.db.acquire() as session:
        stmt = select(HostVerificationSession).where(
            HostVerificationSession.conversation_id == conversation_id
        )
        result = session.execute(stmt)
        host_verification_session = result.scalar()
        if host_verification_session is None:
            return flask.Response("Not found conversation", status=404)
        counter = session.execute(
            select(AccommodationUnit)
            .where(AccommodationUnit.host_id == host_verification_session.host_id)
            .with_only_columns([func.count()])
        ).scalar()
        if counter:
            return JSONResponse("Already exists accommodation", status=409)
        if type(data) != list:
            data = [data]
        for obj in data:
            obj["hostId"] = host_verification_session.host_id
        try:
            accommodations = schema.load(data, session=session)
        except marshmallow.ValidationError as e:
            return JSONResponse(
                {"validationErrors": e.messages},
                status=422,
            )
        session.add_all(accommodations)
        session.commit()
        response = schema_full.dump(accommodations)

    return JSONResponse(response, status=201)
