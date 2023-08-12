"""Check logging library usage"""
# pylint: disable=redefined-outer-name

import io
import re
from typing import Generator
from typing import List

import pytest

import classlogging


@pytest.fixture(scope="session")
def session_log_stream() -> io.StringIO:
    """Prepare global test stream and configure"""

    stream = io.StringIO()
    classlogging.configure_logging(level=classlogging.LogLevel.DEBUG, stream=stream)
    return stream


@pytest.fixture
def test_log_stream(session_log_stream) -> Generator[io.StringIO, None, None]:
    """Give test stream and clear after usage"""
    yield session_log_stream
    session_log_stream.truncate(0)


class PytestLogger(classlogging.LoggerMixin):
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
