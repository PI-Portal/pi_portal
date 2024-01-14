"""CronJobBase class."""

import abc
import logging
import time


class CronJobBase(abc.ABC):
  """An individual cron job, run as a thread.

  :param log: The logging instance for this cron job.
  """

  name: str
  interval: int

  def __init__(self, log: logging.Logger) -> None:
    self.log = log

  def start(self) -> None:
    """Start the cron job."""

    self.log.warning(
        "Cron job '%s' is starting ...",
        self.name,
        extra={"job": self.name},
    )

    while True:
      self.cron()
      time.sleep(self.interval)

  @abc.abstractmethod
  def cron(self) -> None:
    """Cron implementation."""
