"""The task router for Pi Portal."""
import abc
import logging
from typing import TYPE_CHECKING, Dict

from pi_portal.modules.metaclasses.post_init_caller import (
    MetaAbstractPostInitCaller,
)
from pi_portal.modules.tasks.enums import RoutingLabel

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask
  from .queue_base import QueueBase, QueueMetrics


class TaskRouterBase(metaclass=MetaAbstractPostInitCaller):
  """The task router for Pi Portal."""

  queues: Dict["RoutingLabel", "QueueBase"]

  @abc.abstractmethod
  def __init__(self, log: logging.Logger) -> None:
    """Instantiate a queue implementation for each routing label.

    :param log: A logger instance to pass to each queue.
    """

  def __post_init__(self) -> None:
    for routing_label in RoutingLabel:
      assert routing_label in self.queues

  def ack(self, task: "TypeGenericTask") -> None:
    """Ack a task from the corresponding queue.

    :param task: The task to ack.
    """
    self.queues[task.routing_label].ack(task)

  def get(self, routing_label: "RoutingLabel") -> "TypeGenericTask":
    """Return the typed task object from the selected queue.

    :param routing_label: The queue to select.
    :returns: The dequeued task.
    """
    return self.queues[routing_label].get()

  def maintenance(self, routing_label: "RoutingLabel") -> None:
    """Perform queue maintenance tasks on the selected queue.

    :param routing_label: The queue to select.
    """
    self.queues[routing_label].maintenance()

  def metrics(self, routing_label: "RoutingLabel") -> "QueueMetrics":
    """Extract metrics from the selected queue.

    :param routing_label: The queue to select.
    :returns: A collection of metrics for the selected task queue.
    """
    return self.queues[routing_label].metrics()

  def put(self, task: "TypeGenericTask") -> None:
    """Enqueue a task to the corresponding queue.

    :param task: the task to schedule.
    """
    self.queues[task.routing_label].put(task)

  def retry(self, task: "TypeGenericTask") -> None:
    """Retry a failed task on the corresponding queue.

    :param task: the task to schedule.
    """
    self.queues[task.routing_label].retry(task)
