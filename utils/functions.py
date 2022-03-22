import functools
from typing import Optional

from flask import Response, Request as FlaskRequest
from marshmallow import ValidationError
import sentry_sdk

from repos import Repos


class Request(FlaskRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repos: Optional[Repos] = None
        self.user: Optional[dict] = None


def function_wrapper(func):
    """
    Adds repos, user, handles errors.
    """

    @functools.wraps(func)
    def wrapper(request: FlaskRequest):
        try:
            repos = Repos()

            auth_header = request.headers.get("Authorization", "")
            user = repos.users.upsert_from_jwt(auth_header.strip("Bearer").strip())
            if not user:
                return Response(
                    {"message": "Not authenticated."},
                    status=403,
                    mimetype="application/json",
                )

            request.user = user
            request.repos = repos
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
