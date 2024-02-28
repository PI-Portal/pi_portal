"""Test the TaskSchedulerCommand class."""

from unittest import mock

from pi_portal import config
from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine import task_scheduler
from pi_portal.cli_commands.mixins import state


class TestTaskSchedulerCommand:
  """Test the TaskSchedulerCommand class."""

  def test_initialize__inheritance(
      self,
      task_scheduler_command_instance: task_scheduler.TaskSchedulerCommand,
  ) -> None:
    assert isinstance(
        task_scheduler_command_instance,
        state.CommandManagedStateMixin,
    )
    assert isinstance(
        task_scheduler_command_instance,
        command.CommandBase,
    )

  def test_invoke__starts_task_scheduler(
      self,
      task_scheduler_command_instance: task_scheduler.TaskSchedulerCommand,
      mocked_uvicorn: mock.Mock,
  ) -> None:
    task_scheduler_command_instance.invoke()

    mocked_uvicorn.run.assert_called_once_with(
        # pylint: disable=duplicate-code
        "pi_portal.modules.tasks:create_service",
        factory=True,
        uds=config.PI_PORTAL_TASK_MANAGER_SOCKET,
        reload=False,
        workers=1,
        limit_concurrency=config.PI_PORTAL_TASK_MANAGER_CONCURRENCY_LIMIT,
    )
