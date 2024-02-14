"""Test the JsonLoggerConfigurationUnarchived class."""

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
from ..handlers.rotation_unarchived import RotatingFileHandlerUnarchived
from ..json_unarchived import JsonLoggerConfigurationUnarchived


@pytest.mark.usefixtures('test_state')
class TestJsonLoggerConfigurationUnarchived:
  """Test JsonLoggerConfigurationUnarchived class."""

  timestamp = datetime.datetime(
      2012, 1, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
  )

  def test_initialization__attrs(
      self,
      unarchived_json_logger_instance: JsonLoggerConfigurationUnarchived,
  ) -> None:
    assert unarchived_json_logger_instance.format_str == \
        '%(message)%(levelname)%(name)%(asctime)'
    assert unarchived_json_logger_instance.formatter_class == \
           JsonFormatter
    assert unarchived_json_logger_instance.handler_class == \
           RotatingFileHandlerUnarchived

  def test_configure__without_filename__exception(
      self,
      mocked_logger_name: str,
      unarchived_json_logger_instance: JsonLoggerConfigurationUnarchived,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    with pytest.raises(LoggerConfigurationError) as exc:
      unarchived_json_logger_instance.configure(mock_log,)

    assert str(
        exc.value
    ) == (unarchived_json_logger_instance.misconfiguration_exception_message)

  @mock.patch("os.open", mock.mock_open())
  def test_configure__with_filename__creates_correct_formatter(
      self,
      mocked_logger_name: str,
      mocked_logger_file_name: str,
      unarchived_json_logger_instance: JsonLoggerConfigurationUnarchived,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    unarchived_json_logger_instance.configure(
        mock_log,
        mocked_logger_file_name,
    )

    assert isinstance(
        unarchived_json_logger_instance.formatter,
        JsonFormatter,
    )
    assert unarchived_json_logger_instance.handler.formatter == \
           unarchived_json_logger_instance.formatter

  @mock.patch("os.open", mock.mock_open())
  def test_configure__with_filename__creates_correct_handler(
      self,
      mocked_logger_name: str,
      mocked_logger_file_name: str,
      unarchived_json_logger_instance: JsonLoggerConfigurationUnarchived,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    unarchived_json_logger_instance.configure(
        mock_log,
        mocked_logger_file_name,
    )

    assert len(mock_log.handlers) == 1
    assert isinstance(
        unarchived_json_logger_instance.handler,
        RotatingFileHandlerUnarchived,
    )
    assert unarchived_json_logger_instance.handler == \
           mock_log.handlers[0]
    assert (
        unarchived_json_logger_instance.handler.baseFilename
    ) == mocked_logger_file_name

  @freeze_time(timestamp)
  def test_logging__error_message__no_fields(
      self,
      unarchived_json_logger_stdout_instance: logging.Logger,
      mocked_logger_name: str,
      test_state: state.State,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    unarchived_json_logger_stdout_instance.error(test_message)

    expected_timestamp = self.timestamp.astimezone().replace(tzinfo=None)
    assert json.loads(mocked_logger_stream.getvalue()) == {
        "message": test_message,
        "levelname": "ERROR",
        "name": mocked_logger_name,
        "trace_id": test_state.log_uuid,
        "asctime": expected_timestamp.isoformat(" ") + ",000",
    }
