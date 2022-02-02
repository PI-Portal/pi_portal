"""Test the ProcessCommandBase class."""

from typing import Type, cast
from unittest import mock

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_command,
)
from pi_portal.modules.system import supervisor, supervisor_config
from .fixtures import process_command_harness


class ConcreteCLIProcessCommand(process_command.ProcessCommandBase):
  """A testable concrete instance of the ProcessCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  internal_mock = mock.MagicMock()

  def hook_invoker(self) -> None:
    self.internal_mock()


class TestSlackProcessCommandBase(
    process_command_harness.ProcessCommandBaseTestHarness
):
  """Test the ProcessCommandBase class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(self) -> Type[ConcreteCLIProcessCommand]:
    return ConcreteCLIProcessCommand

  def test_invoke_with_error(self) -> None:
    cast(ConcreteCLIProcessCommand, self.instance
        ).internal_mock.side_effect = supervisor.SupervisorException("Boom!")
    self.instance.invoke()
    self.mock_notifier.notify_error.assert_called_once_with()
