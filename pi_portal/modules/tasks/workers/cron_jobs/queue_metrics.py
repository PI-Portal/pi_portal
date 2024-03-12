"""Periodically log metrics for the task queue."""

from typing import TYPE_CHECKING

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base
from pi_portal.modules.tasks.workers.cron_jobs.mixins import metrics_logger

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class CronJob(
    metrics_logger.MetricsLoggerMixin,
    cron_job_base.CronJobBase[non_scheduled.Args]
):
  """Periodically log metrics for the task queue.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = ()

  interval = config.CRON_INTERVAL_QUEUE_METRICS
  name = "Queue Metrics"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""

    for routing_label, queue in scheduler.router.queues.items():
      metrics = queue.metrics()

      self.metrics_logger.log.info(
          "Metrics for the '%s' task queue.",
          routing_label.value,
          extra={
              "cron": self.name,
              "queue": routing_label.value,
              "queue_metrics": metrics._asdict(),
          },
      )
