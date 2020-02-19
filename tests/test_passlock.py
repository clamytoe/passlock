"""
test_passlock.py

Tests for passlock.
"""
import logging

from passlock import __version__

logging.disable(logging.CRITICAL)


def test_version():
    assert __version__ == '0.1.4'
