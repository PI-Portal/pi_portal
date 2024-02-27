"""Test the CommandRequireTaskSchedulerMixin class."""

from unittest import mock

from pi_portal import config
from ..require_task_scheduler import CommandTaskSchedulerMixin


class TestCommandRequireTaskSchedulerMixin:
  """Test the CommandRequireTaskSchedulerMixin class."""

  debug_subtests = [False, True]

  def test_require_task_scheduler__calls_click_echo(
      self,
      command_scheduler_mixin_instance: CommandTaskSchedulerMixin,
      mocked_click: mock.Mock,
  ) -> None:
    command_scheduler_mixin_instance.require_task_scheduler()

    assert mocked_click.echo.mock_calls == [
        mock.call("Waiting for task manager service ... ", nl=False),
        mock.call("Ready!"),
    ]

  def test_require_task_scheduler__calls_file_system(
      self,
      command_scheduler_mixin_instance: CommandTaskSchedulerMixin,
      mocked_file_system: mock.Mock,
  ) -> None:
    command_scheduler_mixin_instance.require_task_scheduler()

    mocked_file_system.assert_called_once_with(
        config.PI_PORTAL_TASK_MANAGER_SOCKET
    )
    mocked_file_system.return_value.wait_until_exists.assert_called_once_with()
