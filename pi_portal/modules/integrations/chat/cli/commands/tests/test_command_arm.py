"""Test the ArmCommand class."""
from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.cli.commands import ArmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcessException,
)
from ..bases import process_management_command
from .conftest import DiskSpaceScenario


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

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(is_running=False),
          DiskSpaceScenario(is_running=True),
      ]
  )
  def test_invoke__vary_is_running__bypasses_process_start_condition(
      self,
      arm_command_instance: ArmCommand,
      mocked_supervisor_process: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_supervisor_process.return_value. \
        is_running.return_value = scenario.is_running

    arm_command_instance.invoke()

    assert arm_command_instance.process.start_condition() is True

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(low_disk_space=False, is_running=False),
          DiskSpaceScenario(low_disk_space=False, is_running=True),
      ]
  )
  def test_invoke__good_disk__vary_is_running__starts_process(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_super_hook_invoker: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_camera_client.return_value.\
        is_disk_space_available.return_value = not scenario.low_disk_space
    mocked_supervisor_process.return_value.\
        is_running.return_value = scenario.is_running

    arm_command_instance.invoke()

    does_start_process = mocked_super_hook_invoker.mock_calls == [mock.call()]
    does_not_start_process = mocked_super_hook_invoker.mock_calls == []

    assert not scenario.is_running == does_start_process
    assert scenario.is_running == does_not_start_process

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(
              low_disk_space=False, is_running=False, exception=False
          ),
          DiskSpaceScenario(
              low_disk_space=False, is_running=False, exception=True
          ),
      ]
  )
  def test_invoke__good_disk__not_running__vary_exception__set_flag(
      self,
      arm_command_instance: ArmCommand,
      mocked_super_hook_invoker: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      mocked_task_scheduler_client: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_supervisor_process.return_value.is_running.return_value = (
        scenario.is_running
    )
    mocked_super_hook_invoker.side_effect = (
        SupervisorProcessException if scenario.exception else None
    )

    arm_command_instance.invoke()

    does_set_flag = (
        mocked_task_scheduler_client.set_flag.mock_calls == [
            mock.call("FLAG_CAMERA_DISABLED_BY_CRON", False),
        ]
    )
    does_not_set_flag = mocked_task_scheduler_client.set_flag.mock_calls == []
    assert not scenario.exception is does_set_flag
    assert scenario.exception is does_not_set_flag

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(low_disk_space=False, is_running=True),
          DiskSpaceScenario(low_disk_space=False, is_running=False),
      ]
  )
  def test_invoke__good_disk__vary_is_running__does_not_notify_disk_space(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_cli_notifier: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_camera_client.return_value.\
        is_disk_space_available.return_value = not scenario.low_disk_space
    mocked_supervisor_process.return_value.is_running.return_value = (
        scenario.is_running
    )

    arm_command_instance.invoke()

    mocked_cli_notifier.return_value.\
        notify_insufficient_disk_space.assert_not_called()

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(low_disk_space=True, is_running=False),
          DiskSpaceScenario(low_disk_space=True, is_running=True),
      ]
  )
  def test_invoke__low_disk__vary_is_running__does_not_start_process(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_super_hook_invoker: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_camera_client.return_value.\
        is_disk_space_available.return_value = not scenario.low_disk_space
    mocked_supervisor_process.return_value.\
        is_running.return_value = scenario.is_running

    arm_command_instance.invoke()

    mocked_super_hook_invoker.assert_not_called()

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(low_disk_space=True, is_running=True),
          DiskSpaceScenario(low_disk_space=True, is_running=False),
      ]
  )
  def test_invoke__low_disk__vary_is_running__notify_disk_space(
      self,
      arm_command_instance: ArmCommand,
      mocked_camera_client: mock.Mock,
      mocked_cli_notifier: mock.Mock,
      mocked_supervisor_process: mock.Mock,
      scenario: DiskSpaceScenario,
  ) -> None:
    mocked_camera_client.return_value. \
      is_disk_space_available.return_value = not scenario.low_disk_space
    mocked_supervisor_process.return_value.is_running.return_value = (
        scenario.is_running
    )

    arm_command_instance.invoke()

    does_notify = (
        mocked_cli_notifier.return_value.notify_insufficient_disk_space.
        mock_calls == [mock.call()]
    )
    does_not_notify = (
        mocked_cli_notifier.return_value.notify_insufficient_disk_space.
        mock_calls == []
    )
    assert not scenario.is_running == does_notify
    assert scenario.is_running == does_not_notify
