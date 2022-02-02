"""Test Harness for the ProcessStatusCommandBase subclasses."""

import abc
from typing import Type, cast

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_status_command,
)
from pi_portal.modules.system import supervisor, supervisor_config
from typing_extensions import Literal
from .process_command_harness import ProcessExtendedCommandBaseTestHarness


class ProcessStatusCommandBaseTestHarness(
    ProcessExtendedCommandBaseTestHarness,
    abc.ABC,
):
  """Test Harness for the ProcessStatusCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  expected_process_command: Literal["uptime", "status"]

  @abc.abstractmethod
  def get_test_class(
      self
  ) -> Type[process_status_command.ProcessStatusCommandBase]:
    """Override to return the correct test class."""

  def test_invoke_no_error(self) -> None:
    self._mocked_process_command().return_value = "test value"
    self.instance.invoke()
    self._mocked_process_command().assert_called_once_with()
    self.assertEqual(
        cast(process_status_command.ProcessStatusCommandBase,
             self.instance).result,
        "test value",
    )

  def test_invoke_supervisor_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor.SupervisorException("Boom!")
    self.instance.invoke()
    self._mocked_notifier().notify_error.assert_called_once_with()
