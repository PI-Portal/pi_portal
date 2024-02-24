"""Test the StatusCommand class."""
from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.cli.commands import StatusCommand
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from ..bases import process_status_command


class TestStatusCommand:
  """Test the StatusCommand class."""

  def test_initialize__attributes(
      self,
      status_command_instance: StatusCommand,
  ) -> None:
    assert status_command_instance.process_name == ProcessList.CAMERA
    assert status_command_instance.process_command == "status"

  def test_initialize__inheritance(
      self,
      status_command_instance: StatusCommand,
  ) -> None:
    assert isinstance(
        status_command_instance,
        process_status_command.ChatProcessStatusCommandBase,
    )

  @pytest.mark.parametrize(
      "test_status",
      [
          ProcessStatus.RUNNING,
          ProcessStatus.STOPPED,
      ],
  )
  def test_invoke__sends_correct_message(
      self,
      status_command_instance: StatusCommand,
      mocked_chat_bot: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      test_status: ProcessStatus,
  ) -> None:
    mocked_supervisor_process.return_value.status.return_value = (
        test_status.value
    )

    status_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        f"Status: {test_status.value}"
    )
