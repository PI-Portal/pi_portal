"""Test the InstallerLoggingConfiguration class."""

import logging
import os.path
from io import StringIO
from unittest import mock

from freezegun import freeze_time
from ..installer import InstallerLoggerConfiguration


class TestInstallerLoggingConfiguration:
  """Test InstallerLoggingConfiguration class."""

  def test_initialization__attrs(
      self,
      installer_logger_configuration_instance: InstallerLoggerConfiguration
  ) -> None:

    assert installer_logger_configuration_instance.format_str == \
           "%(name)s - %(levelname)s - %(message)s"

  def test_configure__stdout(
      self, mocked_logger_name: str,
      installer_logger_configuration_instance: InstallerLoggerConfiguration
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)

    installer_logger_configuration_instance.configure(mock_log)

    assert len(mock_log.handlers) == 1
    assert isinstance(mock_log.handlers[0], logging.StreamHandler)
    assert mock_log.handlers[0].formatter == \
           installer_logger_configuration_instance.formatter

  @mock.patch("os.open", mock.mock_open())
  def test_configure__file(
      self, mocked_logger_name: str,
      installer_logger_configuration_instance: InstallerLoggerConfiguration
  ) -> None:
    mock_log = logging.getLogger(mocked_logger_name)
    mock_file_name = "test.log"

    installer_logger_configuration_instance.configure(mock_log, mock_file_name)

    assert len(mock_log.handlers) == 1
    assert isinstance(mock_log.handlers[0], logging.FileHandler)
    assert mock_file_name == \
        os.path.basename(
            mock_log.handlers[0].baseFilename
        )
    assert mock_log.handlers[0].formatter == \
           installer_logger_configuration_instance.formatter

  @freeze_time("2012-01-14")
  def test_logging__error_message__no_fields(
      self,
      installer_logger_stdout_instance: logging.Logger,
      mocked_logger_name: str,
      mocked_stream: StringIO,
  ) -> None:
    test_message = "test logging message"

    installer_logger_stdout_instance.error(test_message)

    assert mocked_stream.getvalue() == \
        f"{mocked_logger_name} - ERROR - {test_message}\n"
