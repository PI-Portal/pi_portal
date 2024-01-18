"""TaskProcessorBase class."""
import abc
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Generic

from pi_portal.modules.tasks.task.bases.task_base import (
    TaskBase,
    TypeTaskArguments_co,
    TypeTaskResult,
)

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import TaskType


class TaskProcessorBase(Generic[TypeTaskArguments_co, TypeTaskResult], abc.ABC):
  """Processes and updates tasks of a specific type.

  :param log: A logger instance.
  """

  __slots__ = ("log",)

  type: "TaskType"

  def __init__(self, log: logging.Logger) -> None:
    self.log = log

  @abc.abstractmethod
  def _process(
      self,
      task: "TaskBase[TypeTaskArguments_co, TypeTaskResult]",
  ) -> "TypeTaskResult":
    """Override to perform the actual task processing.

    :param task: The task to process.
    """

  def process(
      self,
      task: "TaskBase[TypeTaskArguments_co, TypeTaskResult]",
  ) -> None:
    """Invoke the task capturing any thrown exception internally.

    :param task: The task to process.
    """

    self.log.debug(
        "Processing '%s' ...",
        task,
        extra={
            "task": task.id,
        },
    )
    try:
      task.result = self._process(task)
      task.ok = True
      self.log.debug(
          "Completed '%s'!",
          task,
          extra={
              "task": task.id,
          },
      )
    except Exception as exc:  # pylint: disable=broad-exception-caught
      task.ok = False
      task.result = exc
      self.log.error(
          "Failed: '%s'!",
          task,
          extra={
              "task": task.id,
          },
      )
      self.log.error(
          "Exception",
          exc_info=exc,
          extra={"task": task.id},
      )
    finally:
      task.completed = datetime.now(tz=timezone.utc)

  def recover(
      self,
      task: "TaskBase[TypeTaskArguments_co, TypeTaskResult]",
  ) -> None:
    """Log a message to indicate this partially failed task is recovered.

    :param task: The task to process.
    """

    self.log.warning(
        "Recovered partially finished '%s'!", task, extra={
            "task": task.id,
        }
    )
