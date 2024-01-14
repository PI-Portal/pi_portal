"""Shared test fixtures for the cron job modules tests."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest


@pytest.fixture
def mocked_cron_logger_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_cron_logger(mocked_cron_logger_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_cron_logger_stream)
  handler.setFormatter(
      logging.Formatter('%(levelname)s - %(job)s - %(message)s')
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  return logger
