"""Periodically logs a status message for external monitoring."""

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.queue.bases.router_base import TaskRouterBase
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base


class CronJob(cron_job_base.CronJobBase[non_scheduled.Args]):
  """Periodically logs a status message for external monitoring.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = ()

  interval = config.CRON_INTERVAL_DEAD_MAN_SWITCH
  name = "Dead Man's Switch"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, router: TaskRouterBase) -> None:
    """Cron implementation."""

    self.log.info(
        "ok",
        extra={"cron": self.name},
    )
