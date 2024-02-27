"""The task queue for Pi Portal."""

import abc
import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import RoutingLabel
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class QueueBase(abc.ABC):
  """An abstract queue base class to wrap around implementations."""

  __slots__ = ("log", "routing_label")

  def __init__(
      self,
      log: logging.Logger,
      routing_label: "RoutingLabel",
  ) -> None:
    """:param log:  A logger instance.
    :param routing_label: The routing label of this queue.
    """
    self.log = log
    self.routing_label = routing_label

  @abc.abstractmethod
  def _ack(self, task: "TypeGenericTask") -> None:
    """Override with vendor implementation."""

  @abc.abstractmethod
  def _get(self) -> "TypeGenericTask":
    """Override with vendor implementation."""

  @abc.abstractmethod
  def _maintenance(self) -> None:
    """Override with vendor implementation."""

  @abc.abstractmethod
  def _metrics(self) -> "QueueMetrics":
    """Override with vendor implementation."""

  @abc.abstractmethod
  def _put(self, task: "TypeGenericTask") -> None:
    """Override with vendor implementation."""

  @abc.abstractmethod
  def _retry(self, task: "TypeGenericTask") -> None:
    """Override with vendor implementation."""

  def ack(self, task: "TypeGenericTask") -> None:
    """Ack a task from the queue.

    :param task: the task to ack.
    """
    self._ack(task)
    self.log.debug(
        "Ack: '%s'!",
        task,
        extra={
            "task": task.id,
            "queue": self.routing_label.value,
        },
    )

  def get(self) -> "TypeGenericTask":
    """Return the typed task object.

    :returns: The dequeued task object.
    """
    task = self._get()
    self.log.debug(
        "Dequeued: '%s'!",
        task,
        extra={
            "task": task.id,
            "queue": self.routing_label.value,
        },
    )
    return task

  def maintenance(self) -> None:
    """Perform queue maintenance tasks."""
    self._maintenance()

  def metrics(self) -> "QueueMetrics":
    """Extract queue metrics.

    :returns: A collection of metrics for the task queue.
    """
    return self._metrics()

  def put(self, task: "TypeGenericTask") -> None:
    """Enqueue a task.

    :param task: the task to schedule.
    """
    task.scheduled = datetime.now(tz=timezone.utc)
    self._put(task)
    self.log.debug(
        "Enqueued: '%s'!",
        task,
        extra={
            "task": task.id,
            "queue": self.routing_label.value,
        },
    )

  def retry(self, task: "TypeGenericTask") -> None:
    """Retry a failed task.

    :param task: the task to retry.
    """
    task.completed = None
    task.ok = None
    task.result.value = None
    self._retry(task)
    self.log.debug(
        "Retried: '%s'!",
        task,
        extra={
            "task": task.id,
            "queue": self.routing_label.value,
        }
    )


class QueueMetrics(NamedTuple):
  """A collection of metrics for the task queue."""

  length: int
  acked_length: int
  unacked_length: int
  storage: float
