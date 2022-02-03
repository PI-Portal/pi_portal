"""Test Harness for the SlackProcessStatusCommandBase subclasses."""

from typing import Type, cast

from pi_portal.modules.system import supervisor, supervisor_config
from typing_extensions import Literal
from ... import process_status_command
from .process_command_harness import ProcessCommandBaseTestHarness


class ProcessStatusCommandBaseTestHarness(ProcessCommandBaseTestHarness):
  """Test Harness for the SlackProcessStatusCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  expected_process_command: Literal["uptime", "status"]
  test_class: Type[process_status_command.SlackProcessStatusCommandBase]

  def test_invoke_no_error(self) -> None:
    self._mocked_process_command().return_value = "test value"
    self.instance.invoke()
    self._mocked_process_command().assert_called_once_with()
    self.assertEqual(
        cast(
            process_status_command.SlackProcessStatusCommandBase,
            self.instance,
        ).result,
        "test value",
    )

  def test_invoke_supervisor_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor.SupervisorException("Boom!")
    self.instance.invoke()
    self._mocked_notifier().notify_error.assert_called_once_with()
