"""Periodically logs metrics for external monitoring."""

import shutil
from typing import TYPE_CHECKING, TypedDict

import psutil
from pi_portal import config
from pi_portal.modules.configuration import state
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

    camera_config = state.State().user_config["CAMERA"]
    disk_space = round(
        (camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"] * 1000000) /
        shutil.disk_usage(config.PATH_CAMERA_CONTENT).free,
        2,
    ) * 100
    cpu = psutil.cpu_percent(interval=1, percpu=False)
    memory = psutil.virtual_memory().percent

    print(disk_space)

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
