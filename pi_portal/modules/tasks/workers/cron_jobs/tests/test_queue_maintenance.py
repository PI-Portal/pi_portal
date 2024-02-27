"""Test the queue_maintenance module."""

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.queue_maintenance import Args as QueueArgs
from .. import queue_maintenance
from ..bases import cron_job_base


class TestQueueMaintenanceCronJob:
  """Test the queue_maintenance module."""

  def test_initialize__attributes(
      self,
      queue_maintenance_cron_job_instance: queue_maintenance.CronJob,
  ) -> None:
    assert queue_maintenance_cron_job_instance.interval == \
        config.CRON_INTERVAL_QUEUE_MAINTENANCE
    assert queue_maintenance_cron_job_instance.name == "Queue Maintenance"
    assert queue_maintenance_cron_job_instance.quiet is False
    assert queue_maintenance_cron_job_instance.type == \
        enums.TaskType.QUEUE_MAINTENANCE

  def test_initialize__inheritance(
      self,
      queue_maintenance_cron_job_instance: queue_maintenance.CronJob,
  ) -> None:
    assert isinstance(
        queue_maintenance_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      queue_maintenance_cron_job_instance: queue_maintenance.CronJob,
  ) -> None:
    expected_args = QueueArgs()

    # pylint: disable=protected-access
    assert queue_maintenance_cron_job_instance._args() == expected_args
