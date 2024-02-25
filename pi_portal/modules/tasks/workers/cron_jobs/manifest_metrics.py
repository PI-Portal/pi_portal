"""Periodically log metrics for the task manifests."""

from typing import TYPE_CHECKING

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class CronJob(cron_job_base.CronJobBase[non_scheduled.Args]):
  """Periodically log metrics for the task manifests."""

  __slots__ = ()

  interval = config.CRON_INTERVAL_MANIFEST_METRICS
  name = "Manifest Metrics"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""

    for name, manifest in scheduler.manifests.items():
      metrics = manifest.metrics()

      self.log.info(
          "Metrics for the '%s' task manifest.",
          name.value,
          extra={
              "cron": self.name,
              "metrics": metrics,
          },
      )
