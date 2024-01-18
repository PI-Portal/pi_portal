"""Test the TaskSchedulerService class."""

from unittest import mock

from .. import service


class TestTaskSchedulerService:
  """Test the TaskSchedulerService class."""

  def test_initialize__scheduler(
      self,
      task_scheduler_service_instance: service.TaskSchedulerService,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    assert task_scheduler_service_instance.scheduler == (
        mocked_task_scheduler.return_value
    )
    mocked_task_scheduler.assert_called_once_with()

  def test_initialize__server(
      self,
      task_scheduler_service_instance: service.TaskSchedulerService,
      mocked_api_server: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    assert task_scheduler_service_instance.server == (
        mocked_api_server.return_value
    )
    mocked_api_server.assert_called_once_with(
        mocked_task_scheduler.return_value
    )
