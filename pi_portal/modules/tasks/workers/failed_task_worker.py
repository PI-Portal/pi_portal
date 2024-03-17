"""FailedTaskWorker class."""
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast

from pi_portal.modules.tasks.enums import TaskManifests
from .bases import worker_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.manifest.bases import task_manifest_base
  from pi_portal.modules.tasks.scheduler import TaskScheduler
  from pi_portal.modules.tasks.task.bases import task_base


class FailedTaskWorker(worker_base.WorkerBase):
  """Reschedule failed but retryable tasks.

  :param scheduler: A task scheduler instance.
  """

  __slots__ = (
      "_is_running",
      "log",
      "manifest",
      "router",
  )

  manifest: "task_manifest_base.TaskManifestBase"

  def __init__(
      self,
      scheduler: "TaskScheduler",
  ) -> None:
    self._is_running = True
    self.log = scheduler.log
    self.manifest = scheduler.manifests[TaskManifests.FAILED_TASKS]
    self.router = scheduler.router

  def start(self) -> None:
    """Start the scheduler."""

    self.log.warning("Failed task scheduler is starting ...",)

    while self._is_running:
      time.sleep(1)
      for task in self.manifest.contents:
        if self._is_due(task):
          self.log.info(
              "Rescheduling: '%s' !",
              task,
              extra={
                  "task_id": task.id,
                  "task_type": task.type.value,
              }
          )
          self.router.retry(task)
          self.manifest.remove(task)

  def _is_due(self, task: "task_base.TypeGenericTask") -> bool:
    due_time = cast(datetime, task.completed).timestamp() + task.retry_after
    return datetime.now(tz=timezone.utc).timestamp() >= due_time

  def halt(self) -> None:
    """Gracefully shutdown the scheduler."""
    self._is_running = False
    self.log.warning("Failed task scheduler is shutting down ...",)
