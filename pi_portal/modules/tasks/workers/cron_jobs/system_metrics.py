"""Periodically logs metrics for external monitoring."""

from typing import TYPE_CHECKING, TypedDict

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.system import metrics
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
  """Periodically logs metrics for external monitoring.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = ()

  interval = config.CRON_INTERVAL_SYSTEM_METRICS
  name = "System Metrics"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""

    system_metrics = metrics.SystemMetrics()

    camera_config = state.State().user_config["CAMERA"]
    disk_space = system_metrics.disk_usage_threshold(
        config.PATH_CAMERA_CONTENT,
        camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"],
    )
    cpu = system_metrics.cpu_usage()
    memory = system_metrics.memory_usage()

    self.metrics_logger.log.info(
        "Raspberry Pi system metrics.",
        extra={
            "cron":
                self.name,
            "system_metrics":
                SystemMetrics(
                    camera_disk_space_utilization=disk_space,
                    cpu_utilization=cpu,
                    memory_utilization=memory,
                )
        },
    )


class SystemMetrics(TypedDict):
  """Typed representation of a system metrics entry."""

  camera_disk_space_utilization: float
  cpu_utilization: float
  memory_utilization: float
