"""Archived JSON logging mixin class."""

from pi_portal.modules.configuration.logging.json_archived import (
    JsonLoggerConfigurationArchived,
)
from .bases import write_log_file


class ArchivedLogFileWriter(write_log_file.LogFileWriterBase):
  """Adds archived JSON logging features to an existing class."""

  logging_config_class = JsonLoggerConfigurationArchived
