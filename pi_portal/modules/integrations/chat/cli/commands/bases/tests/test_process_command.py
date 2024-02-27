"""Test the ChatProcessCommandBase class."""

from unittest import mock

from pi_portal.modules.system import supervisor, supervisor_config
from .. import command
from ..process_command import ChatProcessCommandBase


class TestChatProcessCommandBase:
  """Test the ChatProcessCommandBase class."""

  def test_initialize__attributes(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
  ) -> None:
    assert concrete_process_command_instance.process_name == (
        supervisor_config.ProcessList.BOT
    )

  def test_initialize__inheritance(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
  ) -> None:
    assert isinstance(
        concrete_process_command_instance,
        command.ChatCommandBase,
    )
    assert isinstance(
        concrete_process_command_instance,
        ChatProcessCommandBase,
    )

  def test_initialize__bot(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert concrete_process_command_instance.chatbot == mocked_chat_bot

  def test_initialize__notifier(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
      mocked_cli_notifier: mock.Mock,
      mocked_task_scheduler_client: mock.Mock,
  ) -> None:
    assert concrete_process_command_instance.notifier == (
        mocked_cli_notifier.return_value
    )
    mocked_cli_notifier.assert_called_once_with(mocked_task_scheduler_client)

  def test_initialize__supervisor_process(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert concrete_process_command_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        concrete_process_command_instance.process_name
    )

  def test_invoke__calls_mocked_invoker(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
      mocked_process_invoker: mock.Mock,
  ) -> None:
    concrete_process_command_instance.invoke()

    mocked_process_invoker.assert_called_once_with()

  def test_invoke__supervisor_exception__calls_mocked_notifier(
      self,
      concrete_process_command_instance: ChatProcessCommandBase,
      mocked_process_invoker: mock.Mock,
      mocked_cli_notifier: mock.Mock,
  ) -> None:
    mocked_process_invoker.side_effect = supervisor.SupervisorException("Boom!")

    concrete_process_command_instance.invoke()

    mocked_cli_notifier.return_value.notify_error.assert_called_once_with()
