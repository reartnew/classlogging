"""Check logging library usage"""

import io
import re
from typing import List

from classlogging import LoggerMixin


class PytestLogger(LoggerMixin):
    """Test-related log emitter"""


def test_non_configured_trace():
    """Validate trace method presence before configuring"""
    PytestLogger.logger.trace("trace method must be present")


def test_line_emission(test_log_stream: io.StringIO):
    """Validate basic logging scenario for enabled level"""
    PytestLogger.logger.debug("test enabled")
    log_lines: List[str] = test_log_stream.getvalue().splitlines()
    assert len(log_lines) == 1
    assert re.fullmatch(
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} DEBUG \[tests\.test_logging\.PytestLogger] test enabled$",
        log_lines[0],
    )


def test_line_no_emission(test_log_stream: io.StringIO):
    """Validate basic logging scenario for disabled level"""
    PytestLogger.logger.trace("test disabled")
    assert not test_log_stream.getvalue()
