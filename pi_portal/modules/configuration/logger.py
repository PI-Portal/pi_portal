"""Logger configuration."""

import logging
from typing import Any, Dict, Optional

from pi_portal.modules.configuration import state
from pythonjsonlogger import jsonlogger


class LoggingConfiguration:
  """Pi Portal logging configuration."""

  def __init__(self) -> None:
    running_state = state.State()
    self.level = running_state.log_level
    format_str = '%(message)%(levelname)%(name)%(asctime)'
    self.formatter = PiPortalJsonFormatter(running_state.log_uuid, format_str)

  def configure(self, log: logging.Logger, fname: str) -> logging.Logger:
    """Configure application logging.

    :param log: The logger instance to configure.
    :param fname: The path to write logs to.

    :returns: The configured logger instance.
    """

    log.setLevel(self.level)
    log.handlers = []
    handler = logging.FileHandler(fname, delay=True)
    handler.setFormatter(self.formatter)
    log.addHandler(handler)
    return log


class PiPortalJsonFormatter(jsonlogger.JsonFormatter):
  """JSON log formatter for Pi Portal.

  :param trace_id: The unique uuid for this process instance.
  """

  def __init__(self, trace_id: str, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
    self.trace_id = trace_id

  def add_fields(
      self,
      log_record: Dict[str, Any],
      record: logging.LogRecord,
      message_dict: Dict[str, Optional[str]],
  ) -> None:
    """Add custom fields to the base JsonFormatter.

    :param log_record: The Python object that will converted to JSON.
    :param record: The Python LogRecord object generated.
    :param message_dict: The existing message fields configuration.
    """

    super().add_fields(log_record, record, message_dict)
    log_record['trace_id'] = self.trace_id
