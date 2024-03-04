"""Test the JsonFormatter class."""

import json
import logging
from datetime import datetime
from io import StringIO

from freezegun import freeze_time
from ..json import JsonFormatter


class TestJsonFormatter:
  """Test the JsonFormatter class."""

  def test_initialize__attributes(
      self,
      json_formatter_instance: JsonFormatter,
      mocked_trace_id: str,
  ) -> None:
    assert json_formatter_instance.trace_id == mocked_trace_id

  @freeze_time("2012-01-14")
  def test_converter__returns_correct_time_tuple(
      self,
      json_formatter_instance: JsonFormatter,
  ) -> None:
    assert json_formatter_instance.converter(
    ) == (datetime.utcnow().timetuple())

  def test_logging__no_fields__error_message(
      self,
      json_formatted_logger_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_trace_id: str,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    json_formatted_logger_instance.error(test_message)

    assert json.loads(mocked_logger_stream.getvalue()) == {
        "message": test_message,
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": mocked_trace_id,
    }

  def test_logging__extra_field__error_message(
      self,
      json_formatted_logger_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_trace_id: str,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    json_formatted_logger_instance.error(test_message, extra={"foo": "bar"})

    assert json.loads(mocked_logger_stream.getvalue()) == {
        "message": test_message,
        "foo": "bar",
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": mocked_trace_id,
    }
