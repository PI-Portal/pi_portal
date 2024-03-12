"""Test the DisarmCommand class."""

from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.cli.commands import DisarmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcessException,
)
from ..bases import process_management_command
from .conftest import DiskSpaceScenario


class TestDisarmCommand:
  """Test the DisarmCommand class."""

  def test_initialize__attributes(
      self,
      disarm_command_instance: DisarmCommand,
  ) -> None:
    assert disarm_command_instance.process_name == ProcessList.CAMERA
    assert disarm_command_instance.process_command == "stop"

  def test_initialize__inheritance(
      self,
      disarm_command_instance: DisarmCommand,
  ) -> None:
    assert isinstance(
        disarm_command_instance,
        process_management_command.ChatProcessManagementCommandBase,
    )

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(exception=True),
          DiskSpaceScenario(exception=False),
      ]
  )
  def test_invoke__vary_exception__stops_process(
      self, disarm_command_instance: DisarmCommand,
      mocked_super_hook_invoker: mock.Mock, scenario: DiskSpaceScenario
  ) -> None:
    mocked_super_hook_invoker.side_effect = (
        SupervisorProcessException if scenario.exception else None
    )

    disarm_command_instance.invoke()

    mocked_super_hook_invoker.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario", [
          DiskSpaceScenario(exception=True),
          DiskSpaceScenario(exception=False),
      ]
  )
  def test_invoke__vary_exception__flag_is_set(
      self, disarm_command_instance: DisarmCommand,
      mocked_super_hook_invoker: mock.Mock,
      mocked_task_scheduler_client: mock.Mock, scenario: DiskSpaceScenario
  ) -> None:
    mocked_super_hook_invoker.side_effect = (
        SupervisorProcessException if scenario.exception else None
    )

    disarm_command_instance.invoke()

    does_set_flag = (
        mocked_task_scheduler_client.set_flag.mock_calls == [
            mock.call("FLAG_CAMERA_DISABLED_BY_CRON", False),
        ]
    )
    does_not_set_flag = mocked_task_scheduler_client.set_flag.mock_calls == []
    assert not scenario.exception == does_set_flag
    assert scenario.exception == does_not_set_flag
