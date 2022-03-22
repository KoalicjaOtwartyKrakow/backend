import functools
from typing import Optional

from flask import Response, Request as FlaskRequest
from marshmallow import ValidationError
import sentry_sdk

from utils.db import DB
from .auth import upsert_user_from_jwt


class Request(FlaskRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: Optional[DB] = None
        self.user_guid: Optional[str] = None


def function_wrapper(func):
    @functools.wraps(func)
    def wrapper(request: FlaskRequest):
        try:
            auth_header = request.headers.get("Authorization", "")
            db = DB()
            user_guid = upsert_user_from_jwt(
                db, jwt_payload=auth_header.strip("Bearer").strip()
            )
            if user_guid is None:
                return Response(
                    {"message": "Not authenticated."},
                    status=403,
                    mimetype="application/json",
                )

            request.user_guid = user_guid
            request.db = db

            return func(request)
        except ValidationError as e:
            return Response(
                {"validationErrors": e.messages},
                status=422,
                mimetype="application/json",
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()
            return Response(
                {"message": "Internal server error."},
                status=500,
                mimetype="application/json",
            )

    return wrapper
