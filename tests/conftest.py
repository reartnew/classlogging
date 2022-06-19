"""Logging tests preparatory stage"""
# pylint: disable=redefined-outer-name

import io
from typing import Generator

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
