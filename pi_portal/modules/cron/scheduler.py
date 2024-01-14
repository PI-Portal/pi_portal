"""CronScheduler class."""

import sys
from concurrent.futures import FIRST_EXCEPTION, Future, ThreadPoolExecutor, wait
from typing import List

from pi_portal import config
from pi_portal.modules.mixins import write_log_file
from .jobs import cron_jobs


class CronSchedulerException(Exception):
  """Raised when a scheduled cron job fails."""


class CronScheduler(write_log_file.LogFileWriter):
  """Schedules and monitors threaded cron jobs."""

  jobs = cron_jobs
  log_file_path = config.LOG_FILE_CRON_SCHEDULER
  logger_name = "cron"
  name = "scheduler"

  def __init__(self) -> None:
    self.configure_logger()

  def start(self) -> None:
    """Start the scheduler."""

    self.log.warning(
        "Cron scheduler is starting ...",
        extra={"job": self.name},
    )

    with ThreadPoolExecutor() as executor:
      job_futures: List["Future[None]"] = []
      for JobClass in self.jobs:
        job_instance = JobClass(self.log)
        fut = executor.submit(job_instance.start)
        job_futures.append(fut)
      executor.shutdown(wait=False)
    self._wait(job_futures)

  def _wait(self, jobs: List["Future[None]"]) -> None:
    fut = wait(jobs, return_when=FIRST_EXCEPTION)
    for job in fut.done:
      try:
        job.result()
      except Exception as exc:  # pylint: disable=broad-exception-caught
        self._terminate(jobs.index(job), exc)

  def _terminate(
      self,
      index: int,
      exc: Exception,
  ) -> None:
    self.log.error(
        "Job '%s' has failed!",
        self.jobs[index].name,
        extra={"job": self.name},
    )
    self.log.error(
        "Exception",
        exc_info=exc,
        extra={"job": self.jobs[index].name},
    )
    self.log.error(
        "Cron scheduler is now terminating ...",
        extra={"job": self.name},
    )
    sys.exit(127)
