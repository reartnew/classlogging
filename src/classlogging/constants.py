# -*- coding: utf-8 -*-

APP_ROOT_LOGGER: str = "app"
DEFAULT_LOG_FORMAT: str = "%(asctime)s %(levelname)s [%(truncname)s] %(message)s"
DEFAULT_LOG_FORMAT_COLORED: str = "%(asctime)s %(coloredlevelname)s [%(truncname)s] %(message)s"
MIXIN_LOGGER_ATTR: str = "_mixin_sourced_logger"
LOGSTASH_DSN_PREFIX: str = "logstash://"
