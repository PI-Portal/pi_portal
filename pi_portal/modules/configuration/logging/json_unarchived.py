"""JsonLoggerConfigurationUnarchived class."""

from .bases.json_logger import JsonLoggerBase
from .handlers import rotation_unarchived


class JsonLoggerConfigurationUnarchived(JsonLoggerBase):
  """JSON logging configuration for logs that do not require archival."""

  handler_class = rotation_unarchived.RotatingFileHandlerUnarchived
