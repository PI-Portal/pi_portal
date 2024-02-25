"""CronJobBase class."""

import abc
import logging
from typing import TYPE_CHECKING, Generic, TypeVar

from pi_portal.modules.tasks.enums import TaskPriority

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import TaskType
  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.scheduler import TaskScheduler
  from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase

TypeTaskArguments_co = TypeVar(
    "TypeTaskArguments_co", bound="TaskArgsBase", covariant=True
)


class CronJobAlarm(Exception):
  """Raised when a cron job is due."""


class CronJobBase(Generic[TypeTaskArguments_co], abc.ABC):
  """An individual cron job, run as a thread.

  :param log: A logger instance.
  :param registry: A populated task registry instance.
  """

  __slots__ = ("log", "time_remaining", "registered_task")

  interval: int
  name: str
  priority: TaskPriority = TaskPriority.STANDARD
  type: "TaskType"
  quiet = False
  retry_after = 0

  def __init__(self, log: logging.Logger, registry: "TaskRegistry") -> None:
    self.log = log
    self.registered_task = registry.tasks[self.type]
    self.time_remaining = self.interval

  def schedule(self, scheduler: "TaskScheduler") -> None:
    """Schedule a task execution.

    :param scheduler: A task scheduler instance.
    """
    self.time_remaining = self.interval
    self._hook_submit(scheduler)

  def tick(self) -> None:
    """Advance the cron timer."""
    self.time_remaining -= 1
    if self.time_remaining < 1:
      raise CronJobAlarm

  @abc.abstractmethod
  def _args(self) -> "TypeTaskArguments_co":
    """Generate task arguments for scheduling.."""

  def _hook_submit(self, scheduler: "TaskScheduler") -> None:
    """Override to customize job scheduling.

    param scheduler: A task scheduler instance.
    """

    task_class = self.registered_task.TaskClass
    task = task_class(
        args=self._args(),
        priority=self.priority,
        retry_after=self.retry_after,
    )
    scheduler.router.put(task)
