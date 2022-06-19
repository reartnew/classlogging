"""Parameters value namespaces"""


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
