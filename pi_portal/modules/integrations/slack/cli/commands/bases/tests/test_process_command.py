"""Test the SlackProcessCommandBase class."""

from typing import cast
from unittest import mock

from pi_portal.modules.system import supervisor, supervisor_config
from .. import process_command
from .fixtures import simple_process_command_harness


class ConcreteCLIProcessCommand(process_command.SlackProcessCommandBase):
  """A testable concrete instance of the SlackProcessCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  internal_mock = mock.MagicMock()

  def hook_invoker(self) -> None:
    self.internal_mock()


class TestSlackProcessCommandBase(
    simple_process_command_harness.SimpleProcessCommandBaseTestHarness
):
  """Test the SlackProcessCommandBase class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteCLIProcessCommand

  def test_invoke_with_error(self) -> None:
    cast(
        ConcreteCLIProcessCommand,
        self.instance,
    ).internal_mock.side_effect = supervisor.SupervisorException("Boom!")
    self.instance.invoke()
    self.mock_notifier.notify_error.assert_called_once_with()
