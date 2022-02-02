"""Test the ProcessManagementCommandBase class."""

from typing import Type

from pi_portal.modules.integrations.slack_cli.commands.bases import (
    process_management_command,
)
from pi_portal.modules.system import supervisor_config
from typing_extensions import Literal
from .fixtures.process_management_command_harness import (
    ProcessManagementCommandBaseTestHarness,
)


class ConcreteStartCLIProcessCommand(
    process_management_command.ProcessManagementCommandBase
):
  """A concrete instance of the ProcessManagementCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["start"] = "start"


class ConcreteStopCLIProcessCommand(
    process_management_command.ProcessManagementCommandBase
):
  """A concrete instance of the ProcessManagementCommandBase class."""

  process_name = supervisor_config.ProcessList.BOT
  process_command: Literal["stop"] = "stop"


class TestProcessManagementCommandBaseStart(
    ProcessManagementCommandBaseTestHarness
):
  """Test a concrete start instance of ProcessManagementCommandBase."""

  __test__ = True
  expected_process_command: Literal["start"] = "start"
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(
      self
  ) -> Type[process_management_command.ProcessManagementCommandBase]:
    return ConcreteStartCLIProcessCommand


class TestProcessManagementCommandBaseStop(
    ProcessManagementCommandBaseTestHarness
):
  """Test a concrete stop instance of ProcessManagementCommandBase."""

  __test__ = True
  expected_process_command: Literal["stop"] = "stop"
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(
      self
  ) -> Type[process_management_command.ProcessManagementCommandBase]:
    return ConcreteStopCLIProcessCommand
