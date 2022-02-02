"""Test the ProcessStatusCommandBase class."""

from typing import Type

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_status_command,
)
from pi_portal.modules.system import supervisor_config
from typing_extensions import Literal
from .fixtures.process_status_command_harness import (
    ProcessStatusCommandBaseTestHarness,
)


class ConcreteStatusCLIProcessCommand(
    process_status_command.ProcessStatusCommandBase
):
  """A testable concrete instance of the ProcessStatusCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["status"] = "status"


class ConcreteUptimeCLIProcessCommand(
    process_status_command.ProcessStatusCommandBase
):
  """A testable concrete instance of the ProcessStatusCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["uptime"] = "uptime"


class TestProcessManagementCommandBaseStart(
    ProcessStatusCommandBaseTestHarness
):
  """Test a concrete status instance of ProcessStatusCommandBase."""

  __test__ = True
  expected_process_command: Literal["status"] = "status"
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(
      self
  ) -> Type[process_status_command.ProcessStatusCommandBase]:
    return ConcreteStatusCLIProcessCommand


class TestProcessManagementCommandBaseStop(ProcessStatusCommandBaseTestHarness):
  """Test a concrete uptime instance of ProcessStatusCommandBase."""

  __test__ = True
  expected_process_command: Literal["uptime"] = "uptime"
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(
      self
  ) -> Type[process_status_command.ProcessStatusCommandBase]:
    return ConcreteUptimeCLIProcessCommand
