"""Task scheduler mixin for chat CLI commands."""

from typing import Any

from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient


class TaskSchedulerClientMixin:
  """Task scheduler client mixin for chat CLI commands."""

  task_client: TaskSchedulerServiceClient

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.task_client = TaskSchedulerServiceClient()
    super().__init__(*args, **kwargs)
