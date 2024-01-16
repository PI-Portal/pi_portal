"""LoggerConfigurationBase class."""

import abc
import logging
from typing import Optional

from pi_portal.modules.configuration import state
from ..handlers import rotation


class LoggerConfigurationBase(abc.ABC):
  """Pi Portal base logging configuration."""

  format_str: str
  formatter: logging.Formatter
  running_state: state.State

  def __init__(self) -> None:
    self.running_state = state.State()
    self.level = self.running_state.log_level

  def configure(
      self,
      log: logging.Logger,
      file_name: Optional[str] = None,
  ) -> None:
    """Configure application logging.

    :param log: The logger instance to configure.
    :param file_name: The path to write logs to, none for stdout.
    """

    log.setLevel(self.level)
    self.configure_formatter()
    self.configure_handler(log, file_name)

  def configure_handler(
      self, log: logging.Logger, file_name: Optional[str]
  ) -> None:
    """Configure the logger's handler.

    :param log: The logger instance to configure.
    :param file_name: The path to write logs to, none for stdout.
    """

    log.handlers = []
    handler: Optional[logging.Handler]

    if file_name is None:
      handler = logging.StreamHandler()
    else:
      handler = rotation.RotatingFileHandlerWithEnqueue(file_name)

    handler.setFormatter(self.formatter)
    log.addHandler(handler)

  @abc.abstractmethod
  def configure_formatter(self) -> None:
    """Configure the logger's formatter."""
