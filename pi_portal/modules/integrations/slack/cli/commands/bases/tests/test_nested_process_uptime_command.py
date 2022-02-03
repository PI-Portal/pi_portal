"""Test the NestedSlackUptimeCommandBase class."""

from pi_portal.modules.integrations.slack.cli.commands.bases import (
    nested_process_uptime_command,
)
from pi_portal.modules.system import supervisor_config
from .fixtures.nested_process_uptime_command_harness import (
    NestedUptimeCommandBaseTestHarness,
)


class ConcreteNestedUptimeCommand(
    nested_process_uptime_command.NestedSlackUptimeCommandBase,
):
  """A concrete instance of the NestedSlackUptimeCommandBase class."""

  process_name = supervisor_config.ProcessList.MONITOR


class TestNestedUptimeCommandBase(NestedUptimeCommandBaseTestHarness):
  """Test the NestedSlackUptimeCommandBase class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteNestedUptimeCommand
