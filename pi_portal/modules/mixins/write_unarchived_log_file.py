"""Unarchived JSON logging mixin class."""

from pi_portal.modules.configuration.logging.json_unarchived import (
    JsonLoggerConfigurationUnarchived,
)
from .bases import write_log_file


class UnarchivedLogFileWriter(write_log_file.LogFileWriterBase):
  """Adds unarchived JSON logging features to an existing class."""

  logging_config_class = JsonLoggerConfigurationUnarchived
