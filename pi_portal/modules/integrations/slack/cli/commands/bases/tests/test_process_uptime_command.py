"""Test the SlackProcessUptimeCommandBase class."""

from pi_portal.modules.integrations.slack.cli.commands.bases import (
    process_uptime_command,
)
from pi_portal.modules.system import supervisor_config
from .fixtures.process_uptime_command_harness import (
    ProcessUptimeCommandBaseTestHarness,
)


class ConcreteProcessUptimeCommand(
    process_uptime_command.SlackProcessUptimeCommandBase,
):
  """A concrete instance of the SlackProcessUptimeCommandBase class."""

  process_name = supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR


class TestNestedUptimeCommandBase(ProcessUptimeCommandBaseTestHarness):
  """Test the SlackProcessUptimeCommandBase class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.CONTACT_SWITCH_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteProcessUptimeCommand
