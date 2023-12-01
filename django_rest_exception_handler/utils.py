from typing import Any


def fail(error: Any) -> dict:
    """
    This function handles failure scenarios.

    Args:
        error: The error object.

    Returns:
        A dictionary with status, message, and error keys.
    """
    return {'status': False, 'message': 'fail', 'errror': error}
