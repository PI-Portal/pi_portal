"""Test the JsonLoggerConfigurationArchived class."""

import datetime
import json
import logging
from io import StringIO
from unittest import mock

import pytest
from freezegun import freeze_time
from pi_portal.modules.configuration import state
from ..exceptions.configuration import LoggerConfigurationError
from ..formatters.json import JsonFormatter
from ..handlers.rotation_archived import RotatingFileHandlerArchived
from ..json_archived import JsonLoggerConfigurationArchived


class TestJsonLoggerConfigurationArchived:
  """Test JsonLoggerConfigurationArchived class."""

  timestamp = datetime.datetime(
      2012, 1, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
  )

  def test_initialization__attrs(
      self,
      archived_json_logger_instance: JsonLoggerConfigurationArchived,
  ) -> None:
    assert archived_json_logger_instance.format_str == \
        '%(message)%(levelname)%(name)%(asctime)'
    assert archived_json_logger_instance.formatter_class == \
           JsonFormatter
    assert archived_json_logger_instance.handler_class == \
           RotatingFileHandlerArchived

  def test_configure__without_filename__exception(
      self,
      mocked_logger_name: str,
      archived_json_logger_instance: JsonLoggerConfigurationArchived,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    with pytest.raises(LoggerConfigurationError) as exc:
      archived_json_logger_instance.configure(mock_log,)

    assert str(
        exc.value
    ) == (archived_json_logger_instance.misconfiguration_exception_message)

  @mock.patch("os.open", mock.mock_open())
  def test_configure__with_filename__creates_correct_formatter(
      self,
      mocked_logger_name: str,
      mocked_logger_file_name: str,
      archived_json_logger_instance: JsonLoggerConfigurationArchived,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    archived_json_logger_instance.configure(
        mock_log,
        mocked_logger_file_name,
    )

    assert isinstance(
        archived_json_logger_instance.formatter,
        JsonFormatter,
    )
    assert archived_json_logger_instance.handler.formatter == \
           archived_json_logger_instance.formatter

  @mock.patch("os.open", mock.mock_open())
  def test_configure__with_filename__creates_correct_handler(
      self, mocked_logger_name: str, mocked_logger_file_name: str,
      archived_json_logger_instance: JsonLoggerConfigurationArchived
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    archived_json_logger_instance.configure(
        mock_log,
        mocked_logger_file_name,
    )

    assert len(mock_log.handlers) == 1
    assert isinstance(
        archived_json_logger_instance.handler,
        RotatingFileHandlerArchived,
    )
    assert archived_json_logger_instance.handler == \
           mock_log.handlers[0]
    assert (
        archived_json_logger_instance.handler.baseFilename
    ) == mocked_logger_file_name

  @freeze_time(timestamp)
  def test_logging__error_message__no_fields(
      self,
      archived_json_logger_stdout_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_state: state.State,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    archived_json_logger_stdout_instance.info(test_message)

    expected_timestamp = self.timestamp.astimezone().replace(tzinfo=None)
    assert json.loads(mocked_logger_stream.getvalue()) == {
        "message": test_message,
        "levelname": "INFO",
        "name": mocked_logger_name,
        "trace_id": mocked_state.log_uuid,
        "asctime": expected_timestamp.isoformat(" ") + ",000",
    }
