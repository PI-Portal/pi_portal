"""Test the ChatBotCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine import chatbot
from pi_portal.cli_commands.mixins import require_task_scheduler, state


class TestChatBotCommand:
  """Test the ChatBotCommand class."""

  def test_initialize__inheritance(
      self,
      chatbot_command_instance: chatbot.ChatBotCommand,
  ) -> None:
    assert isinstance(
        chatbot_command_instance,
        require_task_scheduler.CommandTaskSchedulerMixin,
    )
    assert isinstance(
        chatbot_command_instance,
        state.CommandManagedStateMixin,
    )
    assert isinstance(
        chatbot_command_instance,
        command.CommandBase,
    )

  def test_invoke__waits_for_task_scheduler(
      self,
      chatbot_command_instance: chatbot.ChatBotCommand,
      mocked_require_task_scheduler: mock.Mock,
  ) -> None:
    chatbot_command_instance.invoke()

    mocked_require_task_scheduler.assert_called_once_with()

  def test_invoke__starts_chatbot(
      self,
      chatbot_command_instance: chatbot.ChatBotCommand,
      mocked_chatbot: mock.Mock,
  ) -> None:
    chatbot_command_instance.invoke()

    mocked_chatbot.assert_called_once_with()
    mocked_chatbot.return_value.start.assert_called_once_with()
