"""Initial configuration routines"""

import logging
import logging.config
import os
import typing as t

from .constants import (
    LogStream,
    LogLevel,
    DEFAULT_BASE_LOGGER,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_FORMAT_COLORED,
)
from .extensions import (
    Logger,
    LogRecord,
)
from .service import module_lock
from .storage import ConfigurationAuxiliaryStorage

__all__ = [
    "configure_logging",
    "update_module",
]


def update_module() -> None:
    """Patch logging module"""
    with module_lock():
        if ConfigurationAuxiliaryStorage.LOGGING_MODULE_IS_PATCHED:
            return
        # Apply patches
        logging.setLoggerClass(Logger)
        logging.setLogRecordFactory(LogRecord)
        logging.addLevelName(Logger.TRACE, "TRACE")
        setattr(logging, "TRACE", Logger.TRACE)
        ConfigurationAuxiliaryStorage.LOGGING_MODULE_IS_PATCHED = True


def configure_logging(
    main_file: t.Optional[str] = None,
    level: str = LogLevel.INFO,
    record_format: t.Optional[str] = None,
    stream: t.Union[str, t.TextIO, None] = LogStream.STDERR,
    colorize: bool = False,
) -> None:
    """Perform all logging configurations"""
    with module_lock():
        if ConfigurationAuxiliaryStorage.HAS_BEEN_CONFIGURED:
            raise RuntimeError("Logging has already been configured")
    update_module()
    with module_lock():
        handlers: t.Dict[str, t.Dict[str, t.Union[str, t.TextIO]]] = {}
        if record_format is not None and colorize:
            raise ValueError("Can't colorize custom record format")

        # Process stdout handler
        if stream is not None:
            handlers["__consoleHandler__"] = {
                "class": "logging.StreamHandler",
                "formatter": "__custom__",
                "stream": stream,
            }

        # Process file handler
        if main_file is not None:
            filename = os.path.realpath(os.path.expanduser(main_file))
            # Prepare container directory
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)
            handlers["__mainFileHandler__"] = {
                "class": "logging.FileHandler",
                "formatter": "__custom__",
                "filename": filename,
            }

        logging.config.dictConfig(
            {
                "version": 1,
                "handlers": handlers,
                "loggers": {
                    DEFAULT_BASE_LOGGER: {
                        "handlers": list(handlers),
                        "level": getattr(logging, level),
                    },
                },
                "formatters": {
                    "__custom__": {
                        "format": record_format or (DEFAULT_LOG_FORMAT_COLORED if colorize else DEFAULT_LOG_FORMAT)
                    },
                },
            }
        )
        ConfigurationAuxiliaryStorage.HAS_BEEN_CONFIGURED = True
