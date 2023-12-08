"""JsonLoggerConfiguration class."""

from .bases.base_logger import LoggerConfigurationBase
from .formatters.json import JsonFormatter


class JsonLoggerConfiguration(LoggerConfigurationBase):
  """JSON logging configuration."""

  format_str = '%(message)%(levelname)%(name)%(asctime)'

  def configure_formatter(self) -> None:
    """Configure the logger's formatter."""

    self.formatter = JsonFormatter(self.running_state.log_uuid, self.format_str)
