"""Service utilities"""

import logging
from contextlib import contextmanager

__all__ = [
    "module_lock",
]


# pylint: disable=protected-access
@contextmanager
def module_lock():
    """Wrap routines into native `logging` package lock"""
    with logging._lock:  # noqa
        yield
