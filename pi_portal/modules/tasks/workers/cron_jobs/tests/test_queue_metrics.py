"""Test the queue_metrics module."""

from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from .. import queue_metrics
from ..bases import cron_job_base


class TestQueueMetricsCronJob:
  """Test the queue_metrics module."""

  log_message = (
      "INFO - None - Queue Metrics - {queue} - {metrics} - "
      "Metrics for the '{queue}' task queue.\n"
  )

  def test_initialize__attributes(
      self,
      queue_metrics_cron_job_instance: queue_metrics.CronJob,
  ) -> None:
    assert queue_metrics_cron_job_instance.interval == \
        config.CRON_INTERVAL_QUEUE_METRICS
    assert queue_metrics_cron_job_instance.name == "Queue Metrics"
    assert queue_metrics_cron_job_instance.quiet is True
    assert queue_metrics_cron_job_instance.type == \
        enums.TaskType.NON_SCHEDULED
    assert queue_metrics_cron_job_instance.priority == \
        enums.TaskPriority.STANDARD

  def test_initialize__inheritance(
      self,
      queue_metrics_cron_job_instance: queue_metrics.CronJob,
  ) -> None:
    assert isinstance(
        queue_metrics_cron_job_instance,
        cron_job_base.CronJobBase,
    )

  def test_args__returns_correct_value(
      self,
      queue_metrics_cron_job_instance: queue_metrics.CronJob,
  ) -> None:
    expected_args = non_scheduled.Args()

    # pylint: disable=protected-access
    assert queue_metrics_cron_job_instance._args() == expected_args

  def test_process__logging(
      self,
      queue_metrics_cron_job_instance: queue_metrics.CronJob,
      mocked_task_router: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_task_router.queues = {
        priority: mock.Mock() for priority in enums.TaskPriority
    }

    queue_metrics_cron_job_instance.schedule(mocked_task_router)

    assert mocked_stream.getvalue() == "".join(
        [
            self.log_message.format(
                task=None,
                queue=priority.value,
                metrics=(
                    mocked_task_router.queues[priority].metrics.return_value.
                    _asdict.return_value
                )
            ) for priority in enums.TaskPriority
        ]
    )

  def test_process__calls_queue_metrics(
      self,
      queue_metrics_cron_job_instance: queue_metrics.CronJob,
      mocked_task_router: mock.Mock,
  ) -> None:
    mocked_task_router.queues = {
        priority: mock.Mock() for priority in enums.TaskPriority
    }

    queue_metrics_cron_job_instance.schedule(mocked_task_router)

    for mocked_queue in mocked_task_router.queues.values():
      mocked_queue.metrics.assert_called_once_with()
