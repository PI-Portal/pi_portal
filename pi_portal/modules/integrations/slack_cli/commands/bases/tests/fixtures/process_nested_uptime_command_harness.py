"""Test Harness for the NestedUptimeCommandBase subclasses."""

import abc
from typing import Type

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_nested_uptime_command,
)
from pi_portal.modules.system import supervisor, supervisor_config
from typing_extensions import Literal
from . import process_status_command_harness


class NestedUptimeCommandBaseTestHarness(
    process_status_command_harness.ProcessStatusCommandBaseTestHarness,
    abc.ABC,
):
  """Test Harness for the NestedUptimeCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  expected_process_command = Literal["uptime"]

  @abc.abstractmethod
  def get_test_class(
      self
  ) -> Type[process_nested_uptime_command.NestedUptimeCommandBase]:
    """Override to return the correct test class."""

  def test_invoke_supervisor_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor.SupervisorException("Boom!")
    with self.assertRaises(supervisor.SupervisorException):
      self.instance.invoke()
    self._mocked_notifier().notify_error.assert_called_once_with()
