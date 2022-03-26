import functools
import json
from typing import Optional

from flask import Response, Request as FlaskRequest
from marshmallow import ValidationError
import sentry_sdk

from kokon.utils.db import DB
from kokon.serializers import UUIDEncoder
from .auth import upsert_user_from_jwt
from kokon.orm import User


class Request(FlaskRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: Optional[DB] = None
        self.user: Optional[User] = None


class JSONResponse(Response):
    def __init__(self, response, status=200, **kwargs):
        if not isinstance(response, str):
            response = json.dumps(response, cls=UUIDEncoder)
        super(JSONResponse, self).__init__(
            response=response, status=status, mimetype="application/json", **kwargs
        )


def function_wrapper(func):
    @functools.wraps(func)
    def wrapper(request: FlaskRequest):
        try:
            # https://cloud.google.com/endpoints/docs/openapi/migrate-to-esp-v2#receiving_auth_results_in_your_api
            jwt_header_encoded = request.headers.get("X-Endpoint-API-UserInfo", "")
            db = DB()
            user = upsert_user_from_jwt(db, jwt_header_encoded)
            if user is None:
                return JSONResponse({"message": "Not authenticated."}, status=403)

            request.user = user
            request.db = db

            return func(request)
        except ValidationError as e:
            return JSONResponse({"validationErrors": e.messages}, status=422)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()
            raise e

    return wrapper