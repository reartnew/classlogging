"""Facility classes"""

import logging
import typing as t
from functools import lru_cache

from .constants import DEFAULT_BASE_LOGGER
from .extensions import Logger
from .configuration import update_module

__all__ = [
    "LoggerMixin",
    "LoggerProperty",
]


class LoggerProperty:
    """Class-level logger property"""

    @staticmethod
    @lru_cache(1)
    def _prepare(caller_type: type) -> Logger:
        update_module()
        logger_name: str = ".".join((DEFAULT_BASE_LOGGER, caller_type.__module__, caller_type.__name__))
        return t.cast(Logger, logging.getLogger(logger_name))

    def __get__(self, caller_instance: t.Any, caller_type: type) -> Logger:
        return self._prepare(caller_type)


class LoggerMixin:
    """Add `logger` property"""

    logger = LoggerProperty()
