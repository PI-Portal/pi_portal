"""Test the SlackProcessManagementCommandBase class."""

from pi_portal.modules.system import supervisor_config
from typing_extensions import Literal
from .. import process_management_command
from .fixtures.process_management_command_harness import (
    ProcessManagementCommandBaseTestHarness,
)


class ConcreteStartCLIProcessCommand(
    process_management_command.SlackProcessManagementCommandBase
):
  """A concrete instance of the SlackProcessManagementCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["start"] = "start"


class ConcreteStopCLIProcessCommand(
    process_management_command.SlackProcessManagementCommandBase
):
  """A concrete instance of the SlackProcessManagementCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["stop"] = "stop"


class TestProcessManagementCommandBaseStart(
    ProcessManagementCommandBaseTestHarness
):
  """Test a concrete start instance of SlackProcessManagementCommandBase."""

  __test__ = True
  expected_process_command: Literal["start"] = "start"
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteStartCLIProcessCommand


class TestProcessManagementCommandBaseStop(
    ProcessManagementCommandBaseTestHarness
):
  """Test a concrete stop instance of SlackProcessManagementCommandBase."""

  __test__ = True
  expected_process_command: Literal["stop"] = "stop"
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteStopCLIProcessCommand
