"""Standard logging mixin class."""

from logging import Logger, getLogger

from pi_portal.modules.configuration.logging.json import JsonLoggerConfiguration


class LogFileWriter:
  """Adds logging features to an existing class."""

  logger_name: str
  log_file_path: str
  log: Logger

  def configure_logger(self) -> None:
    """Configure a standardized logger for this class."""

    self.log = getLogger(self.logger_name)
    logger_configuration = JsonLoggerConfiguration()
    logger_configuration.configure(self.log, self.log_file_path)
