"""Metrics logging cronjob mixin class."""

from pi_portal import config
from pi_portal.modules.metaclasses import post_init_caller
from pi_portal.modules.mixins import write_unarchived_log_file


class MetricsLoggerMixin(metaclass=post_init_caller.MetaAbstractPostInitCaller):
  """Adds a metrics logger to a cron job class."""

  metrics_logger: "MetricsLogger"

  def __post_init__(self) -> None:
    self.metrics_logger = MetricsLogger()


class MetricsLogger(write_unarchived_log_file.UnarchivedLogFileWriter):
  """System metrics log file writer."""

  logger_name = "metrics"
  log_file_path = config.LOG_FILE_METRICS

  def __init__(self) -> None:
    self.configure_logger()
