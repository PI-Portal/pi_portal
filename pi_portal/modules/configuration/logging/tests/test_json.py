"""Test the JsonLoggerConfiguration class."""

import datetime
import json
import logging
import os.path
from io import StringIO
from unittest import mock

from freezegun import freeze_time
from pi_portal.modules.configuration import state
from ..formatters.json import JsonFormatter
from ..json import JsonLoggerConfiguration


class TestJsonLoggerConfiguration:
  """Test JsonLoggerConfiguration class."""

  timestamp = datetime.datetime(
      2012, 1, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
  )

  def test_initialization__attrs(
      self,
      json_logger_configuration_instance: JsonLoggerConfiguration,
  ) -> None:

    assert json_logger_configuration_instance.format_str == \
           '%(message)%(levelname)%(name)%(asctime)'

  def test_configure__stdout(
      self,
      mocked_logger_name: str,
      json_logger_configuration_instance: JsonLoggerConfiguration,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    json_logger_configuration_instance.configure(mock_log)

    assert len(mock_log.handlers) == 1
    assert isinstance(mock_log.handlers[0], logging.StreamHandler)
    assert isinstance(
        json_logger_configuration_instance.formatter, JsonFormatter
    )
    assert mock_log.handlers[0].formatter == \
           json_logger_configuration_instance.formatter

  @mock.patch("os.open", mock.mock_open())
  def test_configure__file(
      self,
      mocked_logger_name: str,
      json_logger_configuration_instance: JsonLoggerConfiguration,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)
    mock_file_name = "test.log"

    json_logger_configuration_instance.configure(mock_log, mock_file_name)

    assert len(mock_log.handlers) == 1
    assert isinstance(mock_log.handlers[0], logging.FileHandler)
    assert isinstance(
        json_logger_configuration_instance.formatter, JsonFormatter
    )
    assert mock_file_name == \
        os.path.basename(
          mock_log.handlers[0].baseFilename
        )
    assert mock_log.handlers[0].formatter == \
           json_logger_configuration_instance.formatter

  @freeze_time(timestamp)
  def test_logging__error_message__no_fields(
      self,
      json_logger_stdout_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_state: state.State,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    json_logger_stdout_instance.error(test_message)

    expected_timestamp = self.timestamp.astimezone().replace(tzinfo=None)
    assert json.loads(mocked_logger_stream.getvalue()) == {
        "message": test_message,
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": mocked_state.log_uuid,
        "asctime": expected_timestamp.isoformat(" ") + ",000",
    }
