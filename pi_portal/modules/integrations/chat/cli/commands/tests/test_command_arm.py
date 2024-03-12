"""Test the ArmCommand class."""
from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.cli.commands import ArmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases import process_management_command


class TestArmCommand:
  """Test the ArmCommand class."""

  def test_initialize__attributes(
      self,
      arm_command_instance: ArmCommand,
  ) -> None:
    assert arm_command_instance.process_name == ProcessList.CAMERA
    assert arm_command_instance.process_command == "start"

  def test_initialize__inheritance(
      self,
      arm_command_instance: ArmCommand,
  ) -> None:
    assert isinstance(
        arm_command_instance,
        process_management_command.ChatProcessManagementCommandBase,
    )

  @pytest.mark.parametrize("low_disk_space", [True, False])
  def test_invoke__sufficient_disk_space__starts_process(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_super_hook_invoker: mock.Mock,
      low_disk_space: bool,
  ) -> None:
    mocked_camera_client.return_value.\
        is_disk_space_available.return_value = not low_disk_space

    arm_command_instance.invoke()

    does_start_process = mocked_super_hook_invoker.mock_calls == [mock.call()]
    does_not_start_process = mocked_super_hook_invoker.mock_calls == []
    assert not low_disk_space == does_start_process
    assert low_disk_space == does_not_start_process

  @pytest.mark.parametrize("low_disk_space", [True, False])
  def test_invoke__insufficient_disk_space__send_notification(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_cli_notifier: mock.Mock,
      low_disk_space: bool,
  ) -> None:
    mocked_camera_client.return_value.\
        is_disk_space_available.return_value = not low_disk_space

    arm_command_instance.invoke()

    does_notify = mocked_cli_notifier.return_value.\
        notify_insufficient_disk_space.mock_calls == [mock.call()]
    does_not_notify = mocked_cli_notifier.return_value.\
        notify_insufficient_disk_space.mock_calls == []
    assert low_disk_space == does_notify
    assert not low_disk_space == does_not_notify
