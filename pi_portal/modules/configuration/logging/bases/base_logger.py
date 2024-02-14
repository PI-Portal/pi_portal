"""LoggerConfigurationBase class."""

import abc
import logging
from typing import ClassVar, Optional, Type

from pi_portal.modules.configuration import state


class LoggerConfigurationBase(abc.ABC):
  """Pi Portal base logging configuration."""

  format_str: str
  formatter: logging.Formatter
  formatter_class: ClassVar[Type[logging.Formatter]]
  handler: logging.Handler
  handler_class: ClassVar[Type[logging.Handler]]
  handler_log_file_path: Optional[str] = None
  running_state: state.State

  def __init__(self) -> None:
    self.running_state = state.State()
    self.level = self.running_state.log_level

  def configure(
      self,
      log: logging.Logger,
      log_file_path: Optional[str] = None,
  ) -> None:
    """Configure application logging.

    :param log: The logger instance to configure.
    :param log_file_path: An optional log file path to configure.
    """

    log.setLevel(self.level)
    log.handlers = []

    self.formatter = self.configure_formatter()
    self.handler_log_file_path = log_file_path
    self.handler = self.configure_handler()
    self.handler.setFormatter(self.formatter)

    log.addHandler(self.handler)

  @abc.abstractmethod
  def configure_formatter(self) -> logging.Formatter:
    """Configure the logger's formatter class."""

  @abc.abstractmethod
  def configure_handler(self) -> logging.Handler:
    """Configure the logger's handler class."""
