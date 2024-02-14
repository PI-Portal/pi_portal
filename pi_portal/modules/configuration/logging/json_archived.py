"""JsonLoggerConfigurationArchived class."""

from .bases.json_logger import JsonLoggerBase
from .handlers import rotation_archived


class JsonLoggerConfigurationArchived(JsonLoggerBase):
  """JSON logging configuration for logs that require archival."""

  handler_class = rotation_archived.RotatingFileHandlerArchived
