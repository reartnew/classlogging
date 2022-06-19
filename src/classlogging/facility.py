"""Logging classes extensions"""

from __future__ import annotations

import logging
import typing as t
from contextlib import contextmanager
from functools import lru_cache

from . import constants as c

__all__ = [
    "LogRecord",
    "Logger",
    "LoggerMixin",
    "module_lock",
    "LoggerProperty",
]


# pylint: disable=protected-access
@contextmanager
def module_lock():
    """Wrap routines into native `logging` package lock"""
    logging._acquireLock()
    try:
        yield
    finally:
        logging._releaseLock()


class LogRecord(logging.LogRecord):
    """Adds extra formatting attributes"""

    _COLOR_MAP: t.Dict[str, str] = {
        "CRITICAL": "\033[31m",
        "FATAL": "\033[31m",
        "ERROR": "\033[31m",
        "WARN": "\033[35m",
        "WARNING": "\033[35m",
        "INFO": "\033[34m",
        "DEBUG": "\033[32m",
        "NOTSET": "\033[37m",
        "TRACE": "\033[33m",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.truncname: str = self.name.split(".", maxsplit=1)[1]
        self.coloredlevelname: str = f"{self._COLOR_MAP[self.levelname]}{self.levelname}\033[0m"


class Logger(logging.Logger):
    """Provides even more detailed debugging method 'trace'"""

    TRACE: int = 5

    def warn(self, msg: t.Any, *args, **kwargs) -> t.NoReturn:
        """Mute implementation"""
        raise NotImplementedError

    # pylint: disable=keyword-arg-before-vararg
    def trace(self, msg: t.Any, *args, **kws) -> None:
        """Ultra-detailed events logging method"""
        if self.isEnabledFor(self.TRACE):
            self._log(self.TRACE, msg, args, **kws)

    def exception(self, msg: object = None, *args, exc_info: bool = True, **kwargs) -> None:  # type: ignore
        """Make `msg` param optional"""
        super().exception("" if msg is None else msg, *args, exc_info=exc_info, **kwargs)


class LoggerProperty:
    """Class-level logger property"""

    @staticmethod
    @lru_cache(1)
    def _prepare(caller_type: type) -> Logger:
        logger_name: str = ".".join((c.DEFAULT_BASE_LOGGER, caller_type.__module__, caller_type.__name__))
        return t.cast(Logger, logging.getLogger(logger_name))

    def __get__(self, caller_instance: t.Any, caller_type: type) -> Logger:
        return self._prepare(caller_type)


class LoggerMixin:
    """Add `logger` property"""

    logger = LoggerProperty()
