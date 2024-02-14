"""Test the LogFileWriterBase mixin class."""

from unittest import mock

from ..write_log_file import LogFileWriterBase


class TestLogFileWriterBase:
  """Test the LogFileWriterBase mixin class."""

  def test__configure_logger__creates_expected_logger(
      self,
      concrete_log_file_writer_instance: LogFileWriterBase,
      mocked_get_logger: mock.Mock,
  ) -> None:
    concrete_log_file_writer_instance.configure_logger()

    mocked_get_logger.assert_called_once_with(
        concrete_log_file_writer_instance.logger_name
    )
    assert concrete_log_file_writer_instance.log == (
        mocked_get_logger.return_value
    )

  def test__configure_logger__configures_json_logger(
      self,
      concrete_log_file_writer_instance: LogFileWriterBase,
      mocked_get_logger: mock.Mock,
      mocked_json_logger_config: mock.Mock,
  ) -> None:
    concrete_log_file_writer_instance.configure_logger()

    mocked_json_logger_config.assert_called_once_with()
    mocked_json_logger_config.return_value.configure.assert_called_once_with(
        mocked_get_logger.return_value,
        concrete_log_file_writer_instance.log_file_path,
    )
