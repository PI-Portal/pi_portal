"""Test the TaskSchedulerUptimeCommand class."""

from unittest import mock

from pi_portal.modules.system import supervisor_config
from ..bases import process_uptime_subcommand
from ..uptime_task_scheduler import TaskSchedulerUptimeCommand


class TestTaskSchedulerUptimeCommand:
  """Test the TaskSchedulerUptimeCommand class."""

  def test_initialize__attributes(
      self,
      uptime_task_scheduler_instance: TaskSchedulerUptimeCommand,
  ) -> None:
    assert uptime_task_scheduler_instance.process_name == (
        supervisor_config.ProcessList.TASK_SCHEDULER
    )

  def test_initialize__inheritance(
      self,
      uptime_task_scheduler_instance: TaskSchedulerUptimeCommand,
  ) -> None:
    assert isinstance(
        uptime_task_scheduler_instance,
        process_uptime_subcommand.ChatProcessUptimeCommandBase,
    )

  def test_initialize__bot(
      self,
      uptime_task_scheduler_instance: TaskSchedulerUptimeCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert uptime_task_scheduler_instance.chatbot == mocked_chat_bot

  def test_initialize__notifier(
      self,
      uptime_task_scheduler_instance: TaskSchedulerUptimeCommand,
      mocked_chat_client: mock.Mock,
      mocked_cli_notifier: mock.Mock,
  ) -> None:
    assert uptime_task_scheduler_instance.notifier == (
        mocked_cli_notifier.return_value
    )
    mocked_cli_notifier.assert_called_once_with(mocked_chat_client)

  def test_initialize__supervisor_process(
      self,
      uptime_task_scheduler_instance: TaskSchedulerUptimeCommand,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert uptime_task_scheduler_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        uptime_task_scheduler_instance.process_name
    )
