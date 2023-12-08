"""Test fixtures for the logging formatters tests."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest
from ..json import JsonFormatter


@pytest.fixture
def mocked_trace_id() -> str:
  return "mockTraceId"


@pytest.fixture
def json_formatted_logger_instance(
    mocked_logger_name: str,
    mocked_stream: StringIO,
    mocked_trace_id: str,
) -> logging.Logger:
  log = logging.getLogger(mocked_logger_name)
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(
      JsonFormatter(mocked_trace_id, '%(message)%(levelname)%(name)'),
  )
  log.handlers = [handler]
  return log
