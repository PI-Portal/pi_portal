"""TaskProcessorBase class."""
import abc
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Generic, Optional, cast

from pi_portal.modules.tasks.task.bases.task_base import (
    TaskBase,
    TypeTaskArguments_co,
    TypeTaskResult,
)

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import TaskType
  from pi_portal.modules.tasks.queue import TaskRouter


class TaskProcessorBase(Generic[TypeTaskArguments_co, TypeTaskResult], abc.ABC):
  """Processes and updates tasks of a specific type.

  :param log: A logger instance.
  """

  __slots__ = (
      "log",
      "router",
  )

  type: "TaskType"

  def __init__(self, log: logging.Logger, router: "TaskRouter") -> None:
    self.log = log
    self.router = router

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

    processing_start_time = datetime.now(tz=timezone.utc)

    self.log.debug(
        "Processing: '%s' ...",
        task,
        extra={
            "task_id": task.id,
            "task_type": task.type,
        },
    )
    try:
      task.ok = True
      task.result.value = self._process(task)
      self.log.debug(
          "Completed: '%s'!",
          task,
          extra={
              "task_id": task.id,
              "task_type": task.type,
          },
      )
    except Exception as exc:  # pylint: disable=broad-exception-caught
      task.ok = False
      task.result.value = exc
      task.completed = datetime.now(tz=timezone.utc)
      self.log.error(
          "Failed: '%s'!",
          task,
          extra={
              "task_id": task.id,
              "task_type": task.type,
          },
      )
      self.log.error(
          "Exception",
          exc_info=exc,
          extra={
              "task_id": task.id,
              "task_type": task.type,
          },
      )
    finally:
      task.completed = datetime.now(tz=timezone.utc)
      self.log_timings(processing_start_time, task)

  def log_timings(
      self,
      processing_start_time: datetime,
      task: "TaskBase[TypeTaskArguments_co, TypeTaskResult]",
  ) -> None:
    """Log a task's timing data with respect to it's processing start time.

    :param processing_start_time: The time at which processing began.
    :param task: The task to log timing data for.
    """

    self.log.debug(
        "Task Timing: '%s'.",
        task,
        extra={
            "task_id":
                task.id,
            "task_type":
                task.type,
            "processing_time":
                self._timing_two_decimal_precision(
                    processing_start_time,
                    task.completed,
                ),
            "scheduled_time":
                self._timing_two_decimal_precision(
                    task.scheduled,
                    processing_start_time,
                ),
            "total_time":
                self._timing_two_decimal_precision(
                    task.created,
                    task.completed,
                )
        },
    )

  def _timing_two_decimal_precision(
      self,
      start_time: Optional[datetime],
      end_time: Optional[datetime],
  ) -> float:
    timing = cast(datetime, end_time) - cast(datetime, start_time)
    return round(timing.total_seconds(), 2)

  def recover(
      self,
      task: "TaskBase[TypeTaskArguments_co, TypeTaskResult]",
  ) -> None:
    """Log a message to indicate this partially failed task is recovered.

    :param task: The task to process.
    """

    self.log.warning(
        "Recovered: '%s'!",
        task,
        extra={
            "task_id": task.id,
            "task_type": task.type,
        }
    )
