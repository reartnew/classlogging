# -*- coding: utf-8 -*-

class LogStream(object):
    STDOUT = "ext://sys.stdout"
    STDERR = "ext://sys.stderr"


class LogLevel(object):
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"
