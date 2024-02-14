"""Shared fixtures for the logging modules tests."""
# pylint: disable=redefined-outer-name

from io import StringIO

import pytest


@pytest.fixture
def mocked_logger_file_name() -> str:
  return "/var/log/mock.log"


@pytest.fixture
def mocked_logger_name() -> str:
  """Return a mock logger name."""
  return "mockLogger"


@pytest.fixture
def mocked_logger_stream() -> StringIO:
  """Return a mock logger stream."""
  return StringIO()
