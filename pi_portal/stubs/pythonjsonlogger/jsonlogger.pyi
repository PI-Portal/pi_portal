"""Stubs for the pythonjsonlogger.jsonlogger package."""

import logging
from typing import Any, Dict, Optional

# isort: off


class JsonFormatter(logging.Formatter):

  def add_fields(
      self, log_record: Dict[str, Any], record: logging.LogRecord,
      message_dict: Dict[str, Optional[str]]
  ) -> None:
    ...
