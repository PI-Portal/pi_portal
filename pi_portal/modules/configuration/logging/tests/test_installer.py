"""Test the InstallerLoggingConfiguration class."""

import logging
from io import StringIO

import pytest
from freezegun import freeze_time
from ..exceptions.configuration import LoggerConfigurationError
from ..installer import InstallerLoggerConfiguration


class TestInstallerLoggingConfiguration:
  """Test InstallerLoggingConfiguration class."""

  def test_initialization__attrs(
      self,
      installer_logger_configuration_instance: InstallerLoggerConfiguration,
  ) -> None:
    assert installer_logger_configuration_instance.format_str == \
           "%(name)s - %(levelname)s - %(message)s"
    assert installer_logger_configuration_instance.formatter_class == \
        logging.Formatter
    assert installer_logger_configuration_instance.handler_class == \
        logging.StreamHandler

  def test_configure__with_filename__exception(
      self,
      mocked_logger_name: str,
      mocked_logger_file_name: str,
      installer_logger_configuration_instance: InstallerLoggerConfiguration,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    with pytest.raises(LoggerConfigurationError) as exc:
      installer_logger_configuration_instance.configure(
          mock_log,
          mocked_logger_file_name,
      )

    assert str(exc.value) == (
        installer_logger_configuration_instance.
        misconfiguration_exception_message
    )

  def test_configure__without_filename__creates_correct_formatter(
      self,
      mocked_logger_name: str,
      installer_logger_configuration_instance: InstallerLoggerConfiguration,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    installer_logger_configuration_instance.configure(mock_log)

    assert isinstance(
        installer_logger_configuration_instance.formatter,
        logging.Formatter,
    )
    assert installer_logger_configuration_instance.handler.formatter == \
           installer_logger_configuration_instance.formatter

  def test_configure__without_filename__creates_correct_handler(
      self,
      mocked_logger_name: str,
      installer_logger_configuration_instance: InstallerLoggerConfiguration,
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    installer_logger_configuration_instance.configure(mock_log)

    assert len(mock_log.handlers) == 1
    assert isinstance(
        installer_logger_configuration_instance.handler,
        logging.StreamHandler,
    )
    assert installer_logger_configuration_instance.handler == \
        mock_log.handlers[0]

  @freeze_time("2012-01-14")
  def test_logging__error_message__no_fields(
      self,
      installer_logger_stdout_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_logger_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    installer_logger_stdout_instance.error(test_message)

    assert mocked_logger_stream.getvalue() == \
        f"{mocked_logger_name} - ERROR - {test_message}\n"
