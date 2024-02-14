"""InstallerLoggerConfiguration class."""

import logging

from .bases.base_logger import LoggerConfigurationBase
from .exceptions.configuration import LoggerConfigurationError


class InstallerLoggerConfiguration(LoggerConfigurationBase):
  """Installer logger configuration."""

  format_str = '%(name)s - %(levelname)s - %(message)s'
  formatter_class = logging.Formatter
  handler_class = logging.StreamHandler
  misconfiguration_exception_message = (
      "Installer loggers must not be configured with a file path."
  )

  def configure_formatter(self) -> logging.Formatter:
    """Configure the logger's formatter class."""

    return self.formatter_class(self.format_str)

  def configure_handler(self) -> logging.Handler:
    """Configure the logger's handler class."""

    if isinstance(self.handler_log_file_path, str):
      raise LoggerConfigurationError(self.misconfiguration_exception_message)

    return self.handler_class()
