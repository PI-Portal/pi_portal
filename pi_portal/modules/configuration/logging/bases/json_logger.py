"""JsonLoggerBase class."""

import logging

from pi_portal.modules.configuration.logging.exceptions.configuration import (
    LoggerConfigurationError,
)
from ..formatters.json import JsonFormatter
from .base_logger import LoggerConfigurationBase


class JsonLoggerBase(LoggerConfigurationBase):
  """JSON logging configuration base class."""

  format_str = '%(message)%(levelname)%(name)%(asctime)'
  formatter_class = JsonFormatter
  handler_log_file_path: str
  misconfiguration_exception_message = (
      "JSON loggers must be configured with a file path."
  )

  def configure_formatter(self) -> logging.Formatter:
    """Configure the logger's formatter class."""

    return self.formatter_class(
        self.running_state.log_uuid,
        self.format_str,
    )

  def configure_handler(self) -> logging.Handler:
    """Configure the logger's handler class."""

    if not isinstance(self.handler_log_file_path, str):
      raise LoggerConfigurationError(self.misconfiguration_exception_message)

    return self.handler_class(self.handler_log_file_path)
