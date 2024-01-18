"""Tests for the Machine CLI."""

import pytest
from ..machine_cli import cli as machine_cli
from .conftest import CliScenarioCreatorArgs, TypeMachineCliScenarioCreator


class TestMachineCLI:
  """Test the Machine CLI."""

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_path="cli_machine.task_scheduler.TaskSchedulerCommand",
          ),
      ],
  )
  def test_task_scheduler__invoke__calls_command_class(
      self,
      scenario_args: CliScenarioCreatorArgs,
      machine_cli_scenario_creator: TypeMachineCliScenarioCreator,
  ) -> None:
    scenario = machine_cli_scenario_creator(scenario_args, machine_cli)

    scenario.invoke()

    scenario.command_mock.assert_called_once_with()
    scenario.command_mock.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_path="cli_machine.task_scheduler.TaskSchedulerCommand",
              debug=True,
          ),
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_path="cli_machine.task_scheduler.TaskSchedulerCommand",
              debug=False,
          )
      ],
  )
  def test_task_scheduler__invoke__calls_loads_state(
      self,
      scenario_args: CliScenarioCreatorArgs,
      machine_cli_scenario_creator: TypeMachineCliScenarioCreator,
  ) -> None:
    scenario = machine_cli_scenario_creator(scenario_args, machine_cli)

    scenario.invoke()

    scenario.load_state_mock.assert_called_once_with(debug=scenario.debug)
