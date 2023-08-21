"""Facility classes"""

import inspect
import typing as t
from functools import lru_cache

from .configuration import update_module
from .extensions import Logger, get_logger
from .constants import ROOT_LOGGER_CLEAN_NAME

__all__ = [
    "LoggerMixin",
    "LoggerProperty",
    "get_module_logger",
    "get_root_logger",
]


class LoggerProperty:
    """Class-level logger property"""

    @staticmethod
    @lru_cache(1)
    def _prepare(caller_type: type) -> Logger:
        update_module()
        return get_logger(f"{caller_type.__module__}.{caller_type.__name__}")

    def __get__(self, caller_instance: t.Any, caller_type: type) -> Logger:
        return self._prepare(caller_type)


class LoggerMixin:
    """Add `logger` property"""

    logger = LoggerProperty()


def get_module_logger() -> Logger:
    """Return the module logger name based on the caller's frame"""
    frame = inspect.currentframe()
    try:
        frame_globals: t.Dict[str, t.Any] = frame.f_back.f_globals  # type: ignore
        logger_name: str = frame_globals["__name__"]
        return get_logger(logger_name)
    finally:
        del frame


def get_root_logger() -> Logger:
    """Return base logger for the whole subsystem"""
    return get_logger(ROOT_LOGGER_CLEAN_NAME)
