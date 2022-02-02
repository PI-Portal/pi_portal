"""Test Harness for the ProcessManagementCommandBase subclasses."""

import abc
from typing import Any, Type

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_management_command,
)
from pi_portal.modules.system import (
    supervisor,
    supervisor_config,
    supervisor_process,
)
from typing_extensions import Literal
from .process_command_harness import ProcessExtendedCommandBaseTestHarness


class ProcessManagementCommandBaseTestHarness(
    ProcessExtendedCommandBaseTestHarness,
    abc.ABC,
):
  """Test Harness for the ProcessManagementCommandBase subclasses."""

  __test__ = False
  expected_process_name: supervisor_config.ProcessList
  expected_process_command: Literal["start", "stop"]

  @abc.abstractmethod
  def get_test_class(
      self
  ) -> Type[process_management_command.ProcessManagementCommandBase]:
    """Override to return the correct test class."""

  def _mocked_invoked_notifier(self) -> Any:
    return getattr(
        self._mocked_notifier(),
        f"notify_{self.get_test_class().process_command}"
    )

  def _mocked_already_notifier(self) -> Any:
    return getattr(
        self._mocked_notifier(),
        f"notify_already_{self.get_test_class().process_command}"
    )

  def test_invoke_no_error(self) -> None:
    self.instance.invoke()
    self._mocked_process_command().assert_called_once_with()
    self._mocked_invoked_notifier().assert_called_once_with()

  def test_invoke_process_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor_process.SupervisorProcessException("Boom!")
    self.instance.invoke()
    self._mocked_invoked_notifier().assert_not_called()
    self._mocked_notifier().notify_error.assert_not_called()
    self._mocked_already_notifier().assert_called_once_with()

  def test_invoke_supervisor_error(self) -> None:
    self._mocked_process_command(
    ).side_effect = supervisor.SupervisorException("Boom!")
    self.instance.invoke()
    self._mocked_invoked_notifier().assert_not_called()
    self._mocked_notifier().notify_error.assert_called_once_with()
