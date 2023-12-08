"""Test the JsonFormatter class."""

import json
import logging
from io import StringIO


class TestJsonFormatter:
  """Test the JsonFormatter class."""

  def test__no_fields__error_message(
      self,
      json_formatted_logger_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_trace_id: str,
      mocked_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    json_formatted_logger_instance.error(test_message)

    assert json.loads(mocked_stream.getvalue()) == {
        "message": test_message,
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": mocked_trace_id,
    }

  def test__extra_field__error_message(
      self,
      json_formatted_logger_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_trace_id: str,
      mocked_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    json_formatted_logger_instance.error(test_message, extra={"foo": "bar"})

    assert json.loads(mocked_stream.getvalue()) == {
        "message": test_message,
        "foo": "bar",
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": mocked_trace_id,
    }
