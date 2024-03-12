"""Periodically check for free disk space below a threshold."""

from typing import TYPE_CHECKING

from pi_portal import config
from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system import supervisor_config, supervisor_process
from pi_portal.modules.tasks import enums, service_client
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base

if TYPE_CHECKING:  # pragma: no cover
  import logging

  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class CronJob(cron_job_base.CronJobBase[non_scheduled.Args]):
  """Periodically check for free disk space below a threshold.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = (
      "camera_client",
      "process",
      "task_scheduler_client",
  )

  interval = config.CRON_INTERVAL_DISK_SPACE
  name = "Disk Space"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED
  low_disk_space_message = (
      "Watch out!  We're running out of disk space!\n"
      "** The camera has been shut off! **"
  )

  def __init__(self, log: "logging.Logger", registry: "TaskRegistry") -> None:
    super().__init__(log, registry)
    self.process = supervisor_process.SupervisorProcess(
        supervisor_config.ProcessList.CAMERA
    )
    self.camera_client = CameraClient(self.log)
    self.task_scheduler_client = service_client.TaskSchedulerServiceClient()

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""

    if self.camera_client.is_disk_space_available():
      return

    self.log.warning(
        "Camera storage disk space is now below the %s MB(s) threshold.",
        self.camera_client.camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"],
        extra={
            "cron": self.name,
        },
    )

    try:
      self.process.stop()
      self.log.warning(
          "Camera has been deactivated due to lack of disk space.",
          extra={
              "cron": self.name,
          },
      )
      self.task_scheduler_client.chat_send_message(self.low_disk_space_message)
    except supervisor_process.SupervisorProcessException:
      pass
