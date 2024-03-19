"""Periodically check for free disk space below a threshold."""

from typing import TYPE_CHECKING, Optional

from pi_portal import config
from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system import supervisor_config
from pi_portal.modules.tasks import enums, flags
from pi_portal.modules.tasks.config import DEFERRED_MESSAGE_PREFIX
from pi_portal.modules.tasks.task import (
    chat_send_message,
    flag_set_value,
    supervisor_process,
)
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base

if TYPE_CHECKING:  # pragma: no cover
  import logging

  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class CronJob(cron_job_base.CronJobBase[supervisor_process.Args]):
  """Periodically check for free disk space below a threshold.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = (
      "camera_client",
      "has_sufficient_disk_space",
      "task_scheduler_client",
      "process",
  )

  interval = config.CRON_INTERVAL_DISK_SPACE
  name = "Disk Space"
  quiet = True
  type = enums.TaskType.SUPERVISOR_PROCESS
  low_disk_space_message = (
      "Watch out!  We're running out of disk space!\n"
      "** The camera has been shut off! **"
  )
  resume_camera_message = (
      "We now have enough disk space to run the camera!\n"
      "** The camera has been reactivated! **"
  )

  def __init__(self, log: "logging.Logger", registry: "TaskRegistry") -> None:
    super().__init__(log, registry)
    self.camera_client = CameraClient(self.log)
    self.has_sufficient_disk_space = True

  def _args(self) -> supervisor_process.Args:
    if self.has_sufficient_disk_space:
      return supervisor_process.Args(
          process=supervisor_config.ProcessList.CAMERA,
          requested_state=supervisor_config.ProcessStatus.RUNNING
      )
    return supervisor_process.Args(
        process=supervisor_config.ProcessList.CAMERA,
        requested_state=supervisor_config.ProcessStatus.STOPPED
    )

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""
    task: Optional[supervisor_process.Task]

    self.has_sufficient_disk_space = (
        self.camera_client.is_disk_space_available()
    )

    if self.has_sufficient_disk_space:
      task = self._sufficient_disk_space()
    else:
      task = self._insufficient_disk_space()

    if task:
      scheduler.router.put(task)

  def _insufficient_disk_space(self) -> Optional[supervisor_process.Task]:

    if flags.Flags.FLAG_CAMERA_DISABLED_BY_CRON:
      return None

    self.log.warning(
        "Camera storage disk space is now below the %s MB(s) threshold.",
        self.camera_client.camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"],
        extra={
            "cron": self.name,
        },
    )

    task = supervisor_process.Task(args=self._args())
    task.on_success.append(
        self._create_deferrable_message(self.low_disk_space_message)
    )
    task.on_success.append(
        flag_set_value.Task(
            args=flag_set_value.Args(
                flag_name="FLAG_CAMERA_DISABLED_BY_CRON",
                value=True,
            ),
            retry_after=30,
        )
    )
    return task

  def _sufficient_disk_space(self) -> Optional[supervisor_process.Task]:

    if not flags.Flags.FLAG_CAMERA_DISABLED_BY_CRON:
      return None

    self.log.info(
        "Camera storage disk space is now above the %s MB(s) threshold.",
        self.camera_client.camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"],
        extra={
            "cron": self.name,
        },
    )

    task = supervisor_process.Task(args=self._args())
    task.on_success.append(
        self._create_deferrable_message(self.resume_camera_message)
    )
    task.on_success.append(
        flag_set_value.Task(
            args=flag_set_value.Args(
                flag_name="FLAG_CAMERA_DISABLED_BY_CRON",
                value=False,
            ),
            retry_after=30,
        )
    )

    return task

  def _create_deferrable_message(self, message: str) -> chat_send_message.Task:
    task = chat_send_message.Task(args=chat_send_message.Args(message=message))
    task.on_failure.append(
        chat_send_message.Task(
            args=chat_send_message.Args(
                message=DEFERRED_MESSAGE_PREFIX + message
            ),
            retry_after=300,
        )
    )
    return task
