"""Module constants"""

DEFAULT_BASE_LOGGER: str = "__classlogging__"
ROOT_LOGGER_CLEAN_NAME: str = ""
DEFAULT_LOG_FORMAT: str = "%(asctime)s %(levelname)s [%(clean_name)s] %(ctx_prefix)s%(message)s"
DEFAULT_LOG_FORMAT_COLORED: str = "%(asctime)s %(colored_level_name)s [%(clean_name)s] %(ctx_prefix)s%(message)s"


class LogStream:
    """Most common logging streams"""

    STDOUT = "ext://sys.stdout"
    STDERR = "ext://sys.stderr"


class LogLevel:
    """Most common logging levels"""

    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"
