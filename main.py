# pylint: disable=fixme,invalid-name,no-member,unused-argument
"""Module containing Google Cloud functions for deployment."""

import functions_framework

from functions import handle_create_host
from functions import accommodation
from functions import host
from functions import guest


@functions_framework.http
def add_accommodation(request):
    """HTTP Cloud Function for posting new accommodation units."""
    return accommodation.handle_add_accommodation(request)


@functions_framework.http
def get_all_accommodations(request):
    """HTTP Cloud Function for getting all available accommodation units."""
    return accommodation.handle_get_all_accommodations(request)


@functions_framework.http
def get_all_guests(request):
    """HTTP Cloud Function for getting all guests."""
    return guest.handle_get_all_guests(request)


@functions_framework.http
def add_guest(request):
    """HTTP Cloud Function for posting new guests."""
    return guest.handle_add_guest(request)


@functions_framework.http
def get_guest_by_id(request):
    """HTTP Cloud Function for getting guest by id."""
    return guest.handle_get_guest_by_id(request)


@functions_framework.http
def get_all_hosts(request):
    """HTTP Cloud Function for getting all hosts."""
    return host.handle_get_all_hosts(request)


@functions_framework.http
def create_host(request):
    """HTTP Cloud Function for posting a new host."""
    return handle_create_host(request)
