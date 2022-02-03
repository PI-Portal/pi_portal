"""Test Harness for the NestedSlackUptimeCommandBase subclasses."""

from typing import Type

from pi_portal.modules.integrations.slack.cli.commands.bases import (
    nested_process_uptime_command,
)
from pi_portal.modules.system import supervisor, supervisor_config
from typing_extensions import Literal
from . import process_status_command_harness


class NestedUptimeCommandBaseTestHarness(
    process_status_command_harness.ProcessStatusCommandBaseTestHarness
):
  """Test Harness for the NestedSlackUptimeCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  expected_process_command = Literal["uptime"]
  test_class: Type[nested_process_uptime_command.NestedSlackUptimeCommandBase]

  def test_invoke_supervisor_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor.SupervisorException("Boom!")
    with self.assertRaises(supervisor.SupervisorException):
      self.instance.invoke()
    self._mocked_notifier().notify_error.assert_called_once_with()
