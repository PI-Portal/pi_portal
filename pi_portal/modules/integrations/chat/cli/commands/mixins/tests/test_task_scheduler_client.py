"""Test the TaskSchedulerClientMixin class."""

from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient
from ..task_scheduler_client import TaskSchedulerClientMixin


class TestTaskSchedulerClientMixin:
  """Test the TaskSchedulerClientMixin class."""

  def test_initialize__task_scheduler_client(
      self,
      concrete_task_scheduler_client_mixin_instance: TaskSchedulerClientMixin,
  ) -> None:
    assert isinstance(
        concrete_task_scheduler_client_mixin_instance, TaskSchedulerClientMixin
    )
    assert isinstance(
        concrete_task_scheduler_client_mixin_instance.task_client,
        TaskSchedulerServiceClient
    )
