from logging import error
from typing import Any

from django.conf import settings
from django.db import connections
from django.http import Http404
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from .utils import fail


def exception_handler(exc: Any, context) -> Response:
    """
    Handle exceptions in the REST API.

    Args:
        exc: The exception that was raised.
        context: The context in which the exception was raised.

    Returns:
        A Response object.

    Raises:
        None
    """
    if isinstance(exc, Http404):
        exc = NotFound('Object not found')
    if isinstance(exc, APIException):
        if exc.status_code == 500 and hasattr(settings, 'LOGGING'):
            error(str(exc))
        return Response(fail(exc.detail), status=exc.status_code)
    else:
        set_rollback()
        if hasattr(settings, 'LOGGING'):
            error(str(exc))
        return Response(fail(str(exc)), status=500)


def set_rollback() -> None:
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)
