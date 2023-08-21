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
    session_log_stream.seek(0)


class PytestLogger(classlogging.LoggerMixin):
    """Test-related log emitter"""


def _match_line(payload: str, line: str) -> bool:
    return bool(
        re.fullmatch(
            rf"^\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}},\d{{3}} "
            rf"DEBUG \[tests\.test_logging\.PytestLogger] {payload}$",
            line,
        )
    )


def test_non_configured_trace():
    """Validate trace method presence before configuring"""
    PytestLogger.logger.trace("trace method must be present")


def test_line_emission(test_log_stream: io.StringIO):
    """Validate basic logging scenario for enabled level"""
    PytestLogger.logger.debug("test enabled")
    log_lines: List[str] = test_log_stream.getvalue().splitlines()
    assert len(log_lines) == 1
    assert _match_line("test enabled", log_lines[0])


def test_line_emission_with_context(test_log_stream: io.StringIO):
    """Validate basic logging scenario for enabled level with context"""
    with PytestLogger.logger.context(a="b"):
        PytestLogger.logger.debug("test ctx")
    PytestLogger.logger.debug("test no ctx")
    log_lines: List[str] = test_log_stream.getvalue().splitlines()
    assert len(log_lines) == 2
    assert _match_line("{a=b} test ctx", log_lines[0])
    assert _match_line("test no ctx", log_lines[1])


def test_line_emission_with_nested_context(test_log_stream: io.StringIO):
    """Validate basic logging scenario for enabled level with nested context"""
    PytestLogger.logger.debug("test no ctx 1")
    with PytestLogger.logger.context(a="b"):
        PytestLogger.logger.debug("test ctx lvl 1.1")
        with PytestLogger.logger.context(c="d"):
            PytestLogger.logger.debug("test ctx lvl 2")
        PytestLogger.logger.debug("test ctx lvl 1.2")
    PytestLogger.logger.debug("test no ctx 2")
    log_lines: List[str] = test_log_stream.getvalue().splitlines()
    assert len(log_lines) == 5
    assert _match_line("test no ctx 1", log_lines[0])
    assert _match_line("{a=b} test ctx lvl 1.1", log_lines[1])
    assert _match_line("{a=b} {c=d} test ctx lvl 2", log_lines[2])
    assert _match_line("{a=b} test ctx lvl 1.2", log_lines[3])
    assert _match_line("test no ctx 2", log_lines[4])


def test_line_no_emission(test_log_stream: io.StringIO):
    """Validate basic logging scenario for disabled level"""
    PytestLogger.logger.trace("test disabled")
    assert not test_log_stream.getvalue()
