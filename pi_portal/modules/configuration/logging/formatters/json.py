"""JsonFormatter class."""

import logging
from typing import Any, Dict, Optional

from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
  """JSON log formatter.

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

    :param log_record: The Python object that will be converted to JSON.
    :param record: The Python LogRecord object generated.
    :param message_dict: The existing message fields configuration.
    """

    super().add_fields(log_record, record, message_dict)
    log_record['trace_id'] = self.trace_id
