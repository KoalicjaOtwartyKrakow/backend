import functools
import json
from typing import Optional

from flask import Response, Request as FlaskRequest
from marshmallow import ValidationError
import sentry_sdk

from kokon.orm import User
from kokon.serializers import UUIDEncoder
from .auth import upsert_user_from_jwt
from .db import DB
from .errors import AppError


class Request(FlaskRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: Optional[DB] = None
        self.user: Optional[User] = None


class JSONResponse(Response):
    def __init__(self, response, status=200, **kwargs):
        if not isinstance(response, str):
            # The json returned here is always returned as the only part of the
            # response, with mimetype set to json. There is no raw interpolation
            # with js happening, so setting ensure_ascii is safe, no risk of XSS.
            #
            # For more context see https://v8.dev/features/subsume-json
            response = json.dumps(response, cls=UUIDEncoder, ensure_ascii=False)
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

            request.user = upsert_user_from_jwt(db, jwt_header_encoded)
            request.db = db

            return func(request)
        except ValidationError as e:
            return JSONResponse({"validationErrors": e.messages}, status=422)
        except AppError as e:
            return JSONResponse({"message": e.message}, status=e.status)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()
            raise e

    return wrapper


def public_function_wrapper(func):
    @functools.wraps(func)
    def wrapper(request: FlaskRequest):
        try:
            db = DB()
            request.db = db
            return func(request)
        except AppError as e:
            return JSONResponse({"message": e.message}, status=e.status)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            sentry_sdk.flush()
            raise e

    return wrapper
