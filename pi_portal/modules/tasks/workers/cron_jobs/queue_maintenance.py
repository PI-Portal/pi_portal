"""Periodically perform maintenance on the task queue."""

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import queue_maintenance
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base


class CronJob(cron_job_base.CronJobBase[queue_maintenance.Args]):
  """Periodically perform maintenance on the task queue."""

  __slots__ = ()

  interval = config.CRON_INTERVAL_QUEUE_MAINTENANCE
  name = "Queue Maintenance"
  type = enums.TaskType.QUEUE_MAINTENANCE

  def _args(self) -> queue_maintenance.Args:
    return queue_maintenance.Args()
