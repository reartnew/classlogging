# -*- coding: utf-8 -*-

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
]


@contextmanager
def module_lock():
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
        self.truncname: str = self.name[(len(c.APP_ROOT_LOGGER) + 1):]
        self.coloredlevelname: str = f"{self._COLOR_MAP[self.levelname]}{self.levelname}\033[0m"


class Logger(logging.Logger):
    """Provides even more detailed debugging method 'trace'"""
    TRACE: int = 5

    def warn(self, msg: t.Any, *args, **kwargs) -> t.NoReturn:
        """Mute implementation"""
        raise NotImplementedError

    def trace(self, msg: t.Any, *args, **kws) -> None:
        """Ultra-detailed events logging method"""
        if self.isEnabledFor(self.TRACE):
            self._log(self.TRACE, msg, args, **kws)

    # TODO: pylint: disable=keyword-arg-before-vararg
    def exception(self, msg: t.Any = None, *args, exc_info: bool = True, **kwargs) -> None:
        super().exception("" if msg is None else msg, *args, exc_info=exc_info, **kwargs)


class LoggerProperty(object):

    @staticmethod
    @lru_cache(1)
    def prepare(caller_type: type) -> Logger:
        logger_name: str = ".".join((c.APP_ROOT_LOGGER, caller_type.__module__, caller_type.__name__))
        return logging.getLogger(logger_name)

    def __get__(self, caller_instance: t.Any, caller_type: type) -> Logger:
        return self.prepare(caller_type)


class LoggerMixin(object):
    logger = LoggerProperty()
