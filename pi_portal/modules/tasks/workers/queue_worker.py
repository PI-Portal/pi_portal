"""QueueWorker class."""
from typing import TYPE_CHECKING

from pi_portal.modules.tasks.enums import TaskManifests, TaskType
from .bases import worker_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import RoutingLabel
  from pi_portal.modules.tasks.scheduler import TaskScheduler
  from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask


class QueueWorker(worker_base.WorkerBase):
  """Queue worker for the task scheduler.

  :param scheduler: A task scheduler instance
  :param routing_label: The routing label used by this queue worker.
  """

  __slots__ = (
      "_is_running",
      "failed_task_manifest",
      "log",
      "registry",
      "router",
      "routing_label",
  )

  do_not_process = [TaskType.NON_SCHEDULED]

  def __init__(
      self,
      scheduler: "TaskScheduler",
      routing_label: "RoutingLabel",
  ) -> None:
    self._is_running = True
    self.failed_task_manifest = scheduler.manifests[TaskManifests.FAILED_TASKS]
    self.log = scheduler.log
    self.registry = scheduler.registry
    self.router = scheduler.router
    self.routing_label = routing_label

  def start(self) -> None:
    """Maintain a continuous flow of tasks to the worker thread."""

    self.log.warning(
        "Worker thread has started ...",
        extra={
            "queue": self.routing_label.value,
        },
    )

    while self._is_running:
      self.consumer()

    self.log.warning(
        "Worker thread has exited!",
        extra={
            "queue": self.routing_label.value,
        },
    )

  def consumer(self) -> None:
    """Fetch the next task from the queue and process it."""

    task = self.router.get(routing_label=self.routing_label)
    if self._should_task_be_processed(task):
      self._do_task_processing(task)
      self._do_task_ack(task)
      self._do_task_success(task)
      self._do_task_failure(task)
    else:
      self._do_task_ack(task)

  def _should_task_be_processed(self, task: "TypeGenericTask") -> bool:
    return task.type not in self.do_not_process

  def _do_task_processing(self, task: "TypeGenericTask") -> None:
    processor_class = self.registry.processors[task.type].ProcessorClass
    processor_instance = processor_class(self.log)
    processor_instance.process(task)

  def _do_task_ack(self, task: "TypeGenericTask") -> None:
    self.router.ack(task)

  def _do_task_success(self, task: "TypeGenericTask") -> None:
    if task.ok:
      for success_task in task.on_success:
        success_task.result.cause = task.result
        self.router.put(success_task)

  def _do_task_failure(self, task: "TypeGenericTask") -> None:
    if not task.ok:
      for failure_task in task.on_failure:
        failure_task.result.cause = task.result
        self.router.put(failure_task)
      if task.retry_after > 0:
        self.log.debug(
            "Failed task '%s' will be rescheduled in %s second(s).",
            task,
            task.retry_after,
            extra={
                "queue": self.routing_label.value,
                "task": task.id,
            },
        )
        self.failed_task_manifest.add(task)

  def halt(self) -> None:
    """Stop the worker from processing further tasks."""
    self._is_running = False
