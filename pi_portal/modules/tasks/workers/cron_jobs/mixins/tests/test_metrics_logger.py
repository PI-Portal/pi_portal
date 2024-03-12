"""Test the MetricsLoggerMixin mixin class."""
import logging

from pi_portal import config
from pi_portal.modules.mixins import write_unarchived_log_file
from .. import metrics_logger


class TestMetricsLogger:
  """Test the MetricsLogger class."""

  def test_initialize__attributes(
      self,
      metrics_logger_instance: metrics_logger.MetricsLogger,
      mocked_metrics_logger: logging.Logger,
  ) -> None:
    assert metrics_logger_instance.log == mocked_metrics_logger
    assert metrics_logger_instance.logger_name == "metrics"
    assert metrics_logger_instance.log_file_path == (config.LOG_FILE_METRICS)

  def test_initialize__inheritance(
      self,
      metrics_logger_instance: metrics_logger.MetricsLogger,
  ) -> None:

    assert isinstance(
        metrics_logger_instance,
        write_unarchived_log_file.UnarchivedLogFileWriter,
    )


class TestMetricsLoggerMixin:
  """Test the MetricsLoggerMixin class."""

  def test_initialize__logger(
      self,
      concrete_metrics_cron_job_instance: metrics_logger.MetricsLoggerMixin,
  ) -> None:
    assert isinstance(
        concrete_metrics_cron_job_instance.metrics_logger,
        metrics_logger.MetricsLogger,
    )

  def test_initialize__inheritance(
      self,
      concrete_metrics_cron_job_instance: metrics_logger.MetricsLoggerMixin,
  ) -> None:
    assert isinstance(
        concrete_metrics_cron_job_instance,
        metrics_logger.MetricsLoggerMixin,
    )
