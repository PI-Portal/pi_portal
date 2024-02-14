"""Standard logging mixin base class."""

from logging import Logger, getLogger
from typing import Type

from pi_portal.modules.configuration.logging.bases import json_logger


class LogFileWriterBase:
  """Standard logging mixin base class."""

  logging_config_class: Type[json_logger.JsonLoggerBase]
  logger_name: str
  log_file_path: str
  log: Logger

  def configure_logger(self) -> None:
    """Configure a standardized logger for this class."""

    self.log = getLogger(self.logger_name)
    logger_configuration = self.logging_config_class()
    logger_configuration.configure(self.log, self.log_file_path)
