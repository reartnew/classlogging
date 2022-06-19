"""Logging classes extensions"""

import logging
import typing as t

__all__ = [
    "LogRecord",
    "Logger",
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


class LogRecord(logging.LogRecord):
    """Adds extra formatting attributes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.truncated_name: str = self.name.split(".", maxsplit=1)[1]
        self.colored_level_name: str = f"\033[{_COLOR_CODE_MAP[self.levelname]}m{self.levelname}\033[0m"


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
