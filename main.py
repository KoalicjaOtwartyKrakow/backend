# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import functions_framework
import sentry_sdk

from kokon.functions import accommodation, guest, host, user

from kokon import settings
from kokon.utils.functions import function_wrapper, public_function_wrapper

# See https://github.com/getsentry/sentry-python/issues/1081
sentry_sdk.init(  # pylint: disable=abstract-class-instantiated # noqa: E0110
    settings.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
)


@functions_framework.http
@function_wrapper
def accommodation_function(request):
    """HTTP Cloud Function for handling accommodations objects."""
    return accommodation.accommodation_function(request)


@functions_framework.http
@function_wrapper
def guest_function(request):
    """HTTP Cloud Function for handling guest objects."""
    return guest.guest_function(request)


@functions_framework.http
@function_wrapper
def host_function(request):
    """HTTP Cloud Function for handling host objects."""
    return host.host_function(request)


@functions_framework.http
@function_wrapper
def get_all_users(request):
    """HTTP Cloud Function for getting all users."""
    return user.handle_get_all_users(request)


@functions_framework.http
@public_function_wrapper
def public_accommodation_function(request):
    """HTTP Cloud Function for self handling accommodations."""
    return accommodation.public_accommodation_function(request)


if __name__ == "__main__":
    from kokon.commands import cli

    cli()
