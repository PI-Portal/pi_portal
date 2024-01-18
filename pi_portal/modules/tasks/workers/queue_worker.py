"""QueueWorker class."""
import logging
import time
from typing import TYPE_CHECKING

from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from .bases import worker_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.queue.bases.queue_base import QueueBase
  from pi_portal.modules.tasks.registration.registry import TaskRegistry
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class QueueWorker(worker_base.WorkerBase):
  """Queue worker for the task scheduler.

  :param priority: The queue priority this worker processes.
  :param queue: The queue instance this worker processes.
  :param registry: An instances of the task registry.
  """

  __slots__ = ("_is_running", "log", "priority", "queue", "registry")

  do_not_process = [TaskType.NON_SCHEDULED]
  retry_cool_off = 5

  def __init__(
      self,
      log: logging.Logger,
      priority: "TaskPriority",
      queue: "QueueBase",
      registry: "TaskRegistry",
  ) -> None:
    self._is_running = True
    self.log = log
    self.priority = priority
    self.queue = queue
    self.registry = registry

  def start(self) -> None:
    """Maintain a continuous flow of tasks to the worker thread."""

    self.log.warning(
        "Worker thread has started ...",
        extra={
            "queue": self.priority.value,
        },
    )

    while self._is_running:
      self.consumer()

    self.log.warning(
        "Worker thread has exited!",
        extra={
            "queue": self.priority.value,
        },
    )

  def consumer(self) -> None:
    """Fetch the next task from the queue and process it."""

    task = self.queue.get()
    if self._should_task_be_processed(task):
      self._do_task_processing(task)
      self._do_task_ack(task)
      self._do_task_success(task)
      self._do_task_failure(task)
    else:
      self._do_task_ack(task)

  def _do_task_ack(self, task: "TypeGenericTask") -> None:
    self.queue.ack(task)

  def _should_task_be_processed(self, task: "TypeGenericTask") -> bool:
    return task.type not in self.do_not_process

  def _do_task_processing(self, task: "TypeGenericTask") -> None:
    processor_class = self.registry.processors[task.type].ProcessorClass
    processor_instance = processor_class(self.log)
    processor_instance.process(task)

  def _do_task_success(self, task: "TypeGenericTask") -> None:
    if task.ok:
      for success_task in task.on_success:
        self.queue.put(success_task)

  def _do_task_failure(self, task: "TypeGenericTask") -> None:
    if not task.ok:
      if task.on_failure:
        for failure_task in task.on_failure:
          self.queue.put(failure_task)
      if task.retry_on_error:
        time.sleep(self.retry_cool_off)
        self.queue.retry(task)

  def halt(self) -> None:
    """Stop the worker from processing further tasks."""
    self._is_running = False
