"""Test the SlackProcessStatusCommandBase class."""

from pi_portal.modules.system import supervisor_config
from typing_extensions import Literal
from .. import process_status_command
from .fixtures.process_status_command_harness import (
    ProcessStatusCommandBaseTestHarness,
)


class ConcreteStatusCLIProcessCommand(
    process_status_command.SlackProcessStatusCommandBase
):
  """A testable concrete instance of the SlackProcessStatusCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["status"] = "status"


class ConcreteUptimeCLIProcessCommand(
    process_status_command.SlackProcessStatusCommandBase
):
  """A testable concrete instance of the SlackProcessStatusCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["uptime"] = "uptime"


class TestProcessManagementCommandBaseStart(
    ProcessStatusCommandBaseTestHarness
):
  """Test a concrete status instance of SlackProcessStatusCommandBase."""

  __test__ = True
  expected_process_command: Literal["status"] = "status"
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteStatusCLIProcessCommand


class TestProcessManagementCommandBaseStop(ProcessStatusCommandBaseTestHarness):
  """Test a concrete uptime instance of SlackProcessStatusCommandBase."""

  __test__ = True
  expected_process_command: Literal["uptime"] = "uptime"
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ConcreteUptimeCLIProcessCommand
