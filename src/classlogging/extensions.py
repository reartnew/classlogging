"""Logging classes extensions"""
from __future__ import annotations

import logging
import typing as t

from .constants import DEFAULT_BASE_LOGGER, ROOT_LOGGER_CLEAN_NAME
from .context import get_context_for_logger, LogContext

__all__ = [
    "LogRecord",
    "Logger",
    "get_logger",
]

_COLOR_CODE_MAP: t.Dict[str, int] = {
    "CRITICAL": 31,
    "FATAL": 31,
    "ERROR": 31,
    "WARN": 35,
    "WARNING": 35,
    "INFO": 34,
    "DEBUG": 32,
    "NOTSET": 37,
    "TRACE": 33,
}


def get_logger(name: str) -> Logger:
    """Get cast logger from clean name"""
    return t.cast(
        Logger,
        logging.getLogger(f"{DEFAULT_BASE_LOGGER}.{name}" if name != ROOT_LOGGER_CLEAN_NAME else DEFAULT_BASE_LOGGER),
    )


class WithCleanName:
    """Utility class adding sanitized logger name"""

    name: str

    def __init__(self) -> None:
        self.clean_name: str = self.name.split(".", maxsplit=1)[1] if "." in self.name else ROOT_LOGGER_CLEAN_NAME


class LogRecord(logging.LogRecord, WithCleanName):
    """Adds extra formatting attributes"""

    def __init__(self, *args, **kwargs):
        logging.LogRecord.__init__(self, *args, **kwargs)
        WithCleanName.__init__(self)
        self.colored_level_name: str = f"\033[{_COLOR_CODE_MAP[self.levelname]}m{self.levelname}\033[0m"
        self.context: t.Optional[dict] = get_context_for_logger(self.name)
        self.ctx_prefix: str = "" if self.context is None else "".join(f"{{{k}={v}}} " for k, v in self.context.items())


class Logger(logging.Logger, WithCleanName):
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

    def context(self, **kwargs) -> LogContext:
        """Obtain context wrapper"""
        return LogContext(logger_name=self.name, **kwargs)

    def __init__(self, *args, **kwargs) -> None:
        logging.Logger.__init__(self, *args, **kwargs)
        WithCleanName.__init__(self)

    def get_superior(self) -> Logger:
        """Get preceding level's logger"""
        if self.name == ROOT_LOGGER_CLEAN_NAME:
            raise ValueError("No superior logger for the root")
        parent_name: str = self.clean_name.rsplit(".", 1)[0] if "." in self.clean_name else ROOT_LOGGER_CLEAN_NAME
        return get_logger(parent_name)
