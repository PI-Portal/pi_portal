"""Cron job worker class."""

import logging
import time
from typing import TYPE_CHECKING, Sequence

from pi_portal.modules.tasks.queue.bases import router_base
from pi_portal.modules.tasks.workers.cron_jobs.bases.cron_job_base import (
    CronJobAlarm,
    CronJobBase,
)
from .bases import worker_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase


class CronWorker(worker_base.WorkerBase):
  """Schedules tasks via a set of cron jobs.

  :param log: A logger instance.
  :param router: The task router to schedule created tasks to.
  :param registry: A populated task registry instance.
  """

  __slots__ = ("_is_running", "jobs", "log", "router")

  def __init__(
      self,
      log: logging.Logger,
      router: router_base.TaskRouterBase,
      registry: "TaskRegistry",
  ) -> None:
    self._is_running = True
    self.jobs: "Sequence[CronJobBase[TaskArgsBase]]" = []
    self.log = log
    self.router = router
    self._initialize_cron_jobs(registry)

  def _initialize_cron_jobs(self, registry: "TaskRegistry") -> None:
    cron_jobs = []
    for registered_cron_job in registry.cron_jobs:
      self.log.warning(
          "Loading cron job '%s' ...",
          registered_cron_job.CronJobClass.name,
          extra={"cron": "Scheduler"},
      )
      cron_jobs.append(registered_cron_job.CronJobClass(self.log, registry))
    self.jobs = cron_jobs

  def start(self) -> None:
    """Start the scheduler."""

    self.log.warning(
        "Cron scheduler is starting ...",
        extra={"cron": "Scheduler"},
    )

    while self._is_running:
      time.sleep(1)
      for cron_job in self.jobs:
        try:
          cron_job.tick()
        except CronJobAlarm:
          try:
            if not cron_job.quiet:
              self.log.info(
                  "Scheduling a '%s' task.",
                  cron_job.name,
                  extra={
                      "cron": "Scheduler",
                  }
              )
            cron_job.schedule(self.router)
          except Exception as exc:  # pylint: disable=broad-exception-caught
            self.log.error(
                "A scheduled '%s' task encountered a critical failure!",
                cron_job.type.value,
                extra={"cron": "Scheduler"},
            )
            self.log.error(
                "Exception",
                exc_info=exc,
                extra={"cron": "Scheduler"},
            )

  def halt(self) -> None:
    """Gracefully shutdown the scheduler."""
    self._is_running = False
    self.log.warning(
        "Cron scheduler is shutting down ...",
        extra={"cron": "Scheduler"},
    )
