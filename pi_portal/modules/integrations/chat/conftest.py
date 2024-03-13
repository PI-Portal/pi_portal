"""Test fixtures for the chat integration."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO

import pytest
from pi_portal.conftest import OptionalFieldsLoggingFilter


class ChatLoggingFilter(OptionalFieldsLoggingFilter):

  optional_fields = [
      "event",
  ]


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_chat_logger(mocked_stream: StringIO) -> logging.Logger:
  # pylint: disable=duplicate-code
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(
      logging.Formatter('%(levelname)s - %(event)s - %(message)s')
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  logger.addFilter(ChatLoggingFilter())

  return logger
