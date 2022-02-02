"""Test the NestedUptimeCommandBase class."""

from typing import Type

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_nested_uptime_command,
)
from pi_portal.modules.system import supervisor_config
from .fixtures.process_nested_uptime_command_harness import (
    NestedUptimeCommandBaseTestHarness,
)


class ConcreteNestedUptimeCommand(
    process_nested_uptime_command.NestedUptimeCommandBase,
):
  """A concrete instance of the NestedUptimeCommandBase class."""

  process_name = supervisor_config.ProcessList.MONITOR


class TestNestedUptimeCommandBase(NestedUptimeCommandBaseTestHarness):
  """Test the NestedUptimeCommandBase class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.MONITOR

  def get_test_class(self) -> Type[ConcreteNestedUptimeCommand]:
    return ConcreteNestedUptimeCommand
