"""Test the DiskCommand class."""

from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.cli.commands import DiskCommand
from ..bases import command


@pytest.mark.usefixtures("test_state")
class TestDiskCommand:
  """Test the DiskCommand class."""

  def test_initialize__inheritance(
      self,
      disk_command_instance: DiskCommand,
  ) -> None:
    assert isinstance(
        disk_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__calls_disk_usage(
      self,
      disk_command_instance: DiskCommand,
      mocked_shutil_module: mock.Mock,
  ) -> None:
    mocked_shutil_module.disk_usage.return_value.free = 5000000

    disk_command_instance.invoke()

    mocked_shutil_module.disk_usage.assert_called_once_with(
        config.PATH_CAMERA_CONTENT
    )

  def test_invoke__sends_correct_message(
      self,
      disk_command_instance: DiskCommand,
      mocked_chat_bot: mock.Mock,
      mocked_shutil_module: mock.Mock,
      test_state: state.State,
  ) -> None:
    mocked_shutil_module.disk_usage.return_value.free = 5000000
    expected_free_space = (
        mocked_shutil_module.disk_usage.return_value.free / 1000000
    )
    threshold_value = (
        test_state.user_config["CAMERA"]["DISK_SPACE_MONITOR"]["THRESHOLD"]
    )

    disk_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client.\
        chat_send_message.assert_called_once_with(
          f"Free space for camera storage: {expected_free_space:.2f} MB.\n"
          f"Minimum required for camera operation is: {threshold_value:.2f} MB."
        )
