"""FailedTaskWorker class."""
import logging
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, cast

from .bases import worker_base

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.manifest.bases import task_manifest_base
  from pi_portal.modules.tasks.queue import TaskRouter
  from pi_portal.modules.tasks.task.bases import task_base


class FailedTaskWorker(worker_base.WorkerBase):
  """Reschedule failed but retryable tasks.

  :params log: The logger instance to use.
  :params router: The task router instance to use.
  :params manifest: The manifest containing failed tasks.
  """

  manifest: "task_manifest_base.TaskManifestBase"

  def __init__(
      self,
      log: logging.Logger,
      router: "TaskRouter",
      manifest: "task_manifest_base.TaskManifestBase",
  ) -> None:
    self.log = log
    self.router = router
    self._is_running = True
    self.manifest = manifest

  def start(self) -> None:
    """Start the scheduler."""

    self.log.warning("Failed task scheduler is starting ...",)

    while self._is_running:
      time.sleep(1)
      for task in self.manifest.contents:
        if self._is_due(task):
          self.log.info("Rescheduling: '%s' !", task, extra={"task": task.id})
          self.router.retry(task)
          self.manifest.remove(task)

  def _is_due(self, task: "task_base.TypeGenericTask") -> bool:
    due_time = cast(datetime, task.completed).timestamp() + task.retry_after
    return datetime.now(tz=timezone.utc).timestamp() >= due_time

  def halt(self) -> None:
    """Gracefully shutdown the scheduler."""
    self._is_running = False
    self.log.warning("Failed task scheduler is shutting down ...",)
