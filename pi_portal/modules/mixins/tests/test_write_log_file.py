"""Test the LogFileWriter mixin class."""

from unittest import mock

from .. import write_log_file


class TestLogFileWriter:
  """Test the LogFileWriter mixin class."""

  def test__configure_logger__json_logger(
      self,
      log_file_writer_instance: write_log_file.LogFileWriter,
      mocked_get_logger: mock.Mock,
      mocked_json_logger: mock.Mock,
  ) -> None:
    log_file_writer_instance.configure_logger()

    mocked_json_logger.assert_called_once_with()
    mocked_json_logger.return_value.configure.assert_called_once_with(
        mocked_get_logger.return_value,
        log_file_writer_instance.log_file_path,
    )

  def test__configure_logger__logger(
      self,
      log_file_writer_instance: write_log_file.LogFileWriter,
      mocked_get_logger: mock.Mock,
  ) -> None:
    log_file_writer_instance.configure_logger()

    mocked_get_logger.assert_called_once_with(
        log_file_writer_instance.logger_name
    )
    assert log_file_writer_instance.log == mocked_get_logger.return_value
