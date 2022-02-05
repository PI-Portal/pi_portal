"""Test Harness for the SlackProcessCommandBase subclasses."""

from typing import Any, Type, Union, cast
from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands.bases import (
    process_management_command,
    process_status_command,
)
from pi_portal.modules.system import supervisor_config, supervisor_process
from .simple_process_command_harness import SimpleProcessCommandBaseTestHarness


class ProcessCommandBaseTestHarness(SimpleProcessCommandBaseTestHarness):
  """Test Harness for SlackProcessCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  test_class: Union[
      Type[process_management_command.SlackProcessManagementCommandBase],
      Type[process_status_command.SlackProcessStatusCommandBase],]

  def _mocked_process_command(self) -> Any:
    return getattr(self._mocked_process(), self.test_class.process_command)

  def _mocked_notifier(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.notifier)

  def test_instantiate(self) -> None:
    instance = self.test_class(self.mock_slack_bot)
    self.assertIsInstance(
        instance.process, supervisor_process.SupervisorProcess
    )
