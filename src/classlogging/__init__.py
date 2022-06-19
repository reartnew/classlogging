"""Class-based logging facility"""

from .configuration import configure_logging
from .constants import LogLevel, LogStream
from .facility import LoggerProperty, LoggerMixin
from .version import __version__
