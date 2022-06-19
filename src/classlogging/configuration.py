"""Initial configuration routines"""

import logging
import logging.config
import os
import typing as t

from . import constants as c
from .enums import LogStream, LogLevel
from .facility import Logger, LogRecord, module_lock
from .storage import ConfigurationAuxiliaryStorage

__all__ = [
    "configure_logging",
]


def configure_logging(
    main_file: t.Optional[str] = None,
    level: str = LogLevel.INFO,
    record_format: t.Optional[str] = None,
    stream: t.Union[str, t.TextIO, None] = LogStream.STDERR,
    colorize: bool = False,
    root_logger_name: t.Optional[str] = None,
) -> None:
    """Perform all logging configurations"""
    with module_lock():
        if ConfigurationAuxiliaryStorage.HAS_BEEN_CONFIGURED:
            raise RuntimeError("Logging has already been configured")

        # Now apply patches
        logging.setLoggerClass(Logger)
        logging.setLogRecordFactory(LogRecord)
        logging.addLevelName(Logger.TRACE, "TRACE")
        setattr(logging, "TRACE", Logger.TRACE)

        if root_logger_name is not None:
            c.DEFAULT_BASE_LOGGER = root_logger_name
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
                    c.DEFAULT_BASE_LOGGER: {
                        "handlers": list(handlers),
                        "level": getattr(logging, level),
                    },
                },
                "formatters": {
                    "__custom__": {
                        "format": record_format or (c.DEFAULT_LOG_FORMAT_COLORED if colorize else c.DEFAULT_LOG_FORMAT)
                    },
                },
            }
        )
        ConfigurationAuxiliaryStorage.HAS_BEEN_CONFIGURED = True
