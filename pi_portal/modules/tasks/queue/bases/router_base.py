"""The task router for Pi Portal."""
import abc
import logging
from typing import TYPE_CHECKING, Dict

from pi_portal.modules.metaclasses.post_init_caller import (
    MetaAbstractPostInitCaller,
)
from pi_portal.modules.tasks.enums import TaskPriority

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask
  from .queue_base import QueueBase, QueueMetrics


class TaskRouterBase(metaclass=MetaAbstractPostInitCaller):
  """The task router for Pi Portal."""

  queues: Dict["TaskPriority", "QueueBase"]

  @abc.abstractmethod
  def __init__(self, log: logging.Logger) -> None:
    """Instantiate a queue implementation for each priority.

    :param log: A logger instance to pass to each queue.
    """

  def __post_init__(self) -> None:
    for priority in TaskPriority:
      assert priority in self.queues

  def ack(self, task: "TypeGenericTask") -> None:
    """Ack a task from the corresponding queue.

    :param task: The task to ack.
    """
    self.queues[task.priority].ack(task)

  def get(self, priority: "TaskPriority") -> "TypeGenericTask":
    """Return the typed task object from the selected queue.

    :param priority: The queue to select.
    :returns: The dequeued task.
    """
    return self.queues[priority].get()

  def maintenance(self, priority: "TaskPriority") -> None:
    """Perform queue maintenance tasks on the selected queue.

    :param priority: The queue to select.
    """
    self.queues[priority].maintenance()

  def metrics(self, priority: "TaskPriority") -> "QueueMetrics":
    """Extract metrics from the selected queue.

    :param priority: The queue to select.
    :returns: A collection of metrics for the selected task queue.
    """
    return self.queues[priority].metrics()

  def put(self, task: "TypeGenericTask") -> None:
    """Enqueue a task to the corresponding queue.

    :param task: the task to schedule.
    """
    self.queues[task.priority].put(task)

  def retry(self, task: "TypeGenericTask") -> None:
    """Retry a failed task on the corresponding queue.

    :param task: the task to schedule.
    """
    self.queues[task.priority].retry(task)
