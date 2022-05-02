# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import functions_framework
import sentry_sdk

from kokon.functions import accommodation, guest, host, user

from kokon import settings
from kokon.utils.functions import function_wrapper


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
def add_accommodation(request):
    """HTTP Cloud Function for posting new accommodation units."""
    return accommodation.handle_add_accommodation(request)


@functions_framework.http
@function_wrapper
def get_all_accommodations(request):
    """HTTP Cloud Function for getting all available accommodation units."""
    return accommodation.handle_get_all_accommodations(request)


@functions_framework.http
@function_wrapper
def delete_accommodation(request):
    """HTTP Cloud Function for deleting an accommodation unit."""
    return accommodation.handle_delete_accommodation(request)


@functions_framework.http
@function_wrapper
def get_accommodation_by_id(request):
    """HTTP Cloud Function for getting an accommodation unit."""
    return accommodation.handle_get_accommodation_by_id(request)


@functions_framework.http
@function_wrapper
def update_accommodation(request):
    """HTTP Cloud function for updating an accommodation unit."""
    return accommodation.handle_update_accommodation(request)


@functions_framework.http
@function_wrapper
def get_all_guests(request):
    """HTTP Cloud Function for getting all guests."""
    return guest.handle_get_all_guests(request)


@functions_framework.http
@function_wrapper
def add_guest(request):
    """HTTP Cloud Function for posting new guests."""
    return guest.handle_add_guest(request)


@functions_framework.http
@function_wrapper
def get_guest_by_id(request):
    """HTTP Cloud Function for getting selected guests."""
    return guest.handle_get_guest_by_id(request)


@functions_framework.http
@function_wrapper
def delete_guest(request):
    """HTTP Cloud Function for deleting selected guests."""
    return guest.handle_delete_guest(request)


@functions_framework.http
@function_wrapper
def update_guest(request):
    """HTTP Cloud Function for updating selected guests."""
    return guest.handle_update_guest(request)


@functions_framework.http
@function_wrapper
def get_all_hosts(request):
    """HTTP Cloud Function for getting all hosts."""
    return host.handle_get_all_hosts(request)


@functions_framework.http
@function_wrapper
def delete_host(request):
    """HTTP Cloud Function for deleting a host with a given id."""
    return host.handle_delete_host(request)


@functions_framework.http
@function_wrapper
def update_host(request):
    """HTTP Cloud Function for updating a host."""
    return host.handle_update_host(request)


@functions_framework.http
@function_wrapper
def add_host(request):
    """HTTP Cloud Function for posting a new host."""
    return host.handle_add_host(request)


@functions_framework.http
@function_wrapper
def get_host_by_id(request):
    """HTTP Cloud Function for getting a host with a given id."""
    return host.handle_get_host_by_id(request)


@functions_framework.http
@function_wrapper
def get_all_users(request):
    """HTTP Cloud Function for getting all users."""
    return user.handle_get_all_users(request)


@functions_framework.http
@function_wrapper
def registration(request):
    """HTTP Cloud Function for host registration."""
    return host.handle_registration(request)


if __name__ == "__main__":
    from kokon.commands import cli

    cli()
