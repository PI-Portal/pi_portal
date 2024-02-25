"""Periodically logs a status message for external monitoring."""

from typing import TYPE_CHECKING

from pi_portal import config
from pi_portal.modules.mixins import write_unarchived_log_file
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import non_scheduled
from pi_portal.modules.tasks.workers.cron_jobs.bases import cron_job_base

if TYPE_CHECKING:  # pragma: no cover
  import logging

  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.scheduler import TaskScheduler


class CronJob(cron_job_base.CronJobBase[non_scheduled.Args]):
  """Periodically logs a status message for external monitoring.

  Rather than send a job to queue, this simple job runs directly.
  """

  __slots__ = ("isolated_logger",)

  interval = config.CRON_INTERVAL_DEAD_MAN_SWITCH
  isolated_logger: "DeadManSwitchLogger"
  name = "Dead Man's Switch"
  quiet = True
  type = enums.TaskType.NON_SCHEDULED

  def __init__(self, log: "logging.Logger", registry: "TaskRegistry") -> None:
    super().__init__(log, registry)
    self.isolated_logger = DeadManSwitchLogger()

  def _args(self) -> non_scheduled.Args:
    return non_scheduled.Args()

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Cron implementation."""

    self.isolated_logger.log.info(
        "ok",
        extra={"cron": self.name},
    )


class DeadManSwitchLogger(write_unarchived_log_file.UnarchivedLogFileWriter):
  """Dead man's switch log file writer."""

  logger_name = "dead_man_switch"
  log_file_path = config.LOG_FILE_DEAD_MAN_SWITCH

  def __init__(self) -> None:
    self.configure_logger()
