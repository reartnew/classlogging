"""Logging tests preparatory stage"""

import sys
from pathlib import Path


def pytest_sessionstart():
    """Add sources to sys.path"""
    source_dir: Path = Path(__file__).parents[1] / "src"
    assert source_dir.is_dir()
    sys.path.append(str(source_dir))
