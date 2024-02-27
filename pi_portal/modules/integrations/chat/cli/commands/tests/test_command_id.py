"""Test the IDCommand class."""

from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.cli.commands import IDCommand
from ..bases import command


@pytest.mark.usefixtures("test_state")
class TestIDCommand:
  """Test the IDCommand class."""

  def test_initialize__inheritance(
      self,
      id_command_instance: IDCommand,
  ) -> None:
    assert isinstance(
        id_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__sends_correct_message(
      self,
      id_command_instance: IDCommand,
      mocked_chat_bot: mock.Mock,
      test_state: state.State,
  ) -> None:
    id_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client.\
        chat_send_message.assert_called_once_with(
          f"ID: {test_state.log_uuid}"
        )
