"""Test the manifest_metrics module."""

from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from .. import manifest_metrics
from ..bases import cron_job_base


class TestManifestMetricsCronJob:
  """Test the manifest_metrics module."""

  log_message = (
      "INFO - None - Manifest Metrics - {metrics} - "
      "Metrics for the '{manifest}' task manifest.\n"
  )

  def test_initialize__attributes(
      self,
      manifest_metrics_cron_job_instance: manifest_metrics.CronJob,
  ) -> None:
    assert manifest_metrics_cron_job_instance.interval == \
        config.CRON_INTERVAL_MANIFEST_METRICS
    assert manifest_metrics_cron_job_instance.name == "Manifest Metrics"
    assert manifest_metrics_cron_job_instance.quiet is True
    assert manifest_metrics_cron_job_instance.type == \
        enums.TaskType.NON_SCHEDULED

  def test_initialize__inheritance(
      self,
      manifest_metrics_cron_job_instance: manifest_metrics.CronJob,
  ) -> None:
    assert isinstance(
        manifest_metrics_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      manifest_metrics_cron_job_instance: manifest_metrics.CronJob,
  ) -> None:
    expected_args = non_scheduled.Args()

    # pylint: disable=protected-access
    assert manifest_metrics_cron_job_instance._args() == expected_args

  def test_process__logging(
      self,
      manifest_metrics_cron_job_instance: manifest_metrics.CronJob,
      mocked_task_scheduler: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_task_scheduler.manifests = {
        manifest: mock.Mock() for manifest in enums.TaskManifests
    }

    manifest_metrics_cron_job_instance.schedule(mocked_task_scheduler)

    assert mocked_stream.getvalue() == "".join(
        [
            self.log_message.format(
                manifest=manifest.value,
                metrics=mocked_task_scheduler.manifests[manifest].metrics.
                return_value,
            ) for manifest in enums.TaskManifests
        ]
    )
