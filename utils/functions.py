import functools

from flask import Response
from marshmallow import ValidationError
import sentry_sdk

from repos import Repos


def function_wrapper(func):
    """
    Adds repos, user, handles errors.
    """
    @functools.wraps(func)
    def wrapper(request):
        try:
            repos = Repos()
            request.repos = repos
            # TODO: extract jwt from request
            # request.user = repos.users.upsert_from_jwt(request.headers['...'])
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
