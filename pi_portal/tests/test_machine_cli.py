"""Tests for the Machine CLI."""

import pytest
from ..cli_machine import cli as machine_cli
from .conftest import (
    CliScenarioCreatorArgs,
    TypeCliScenarioCreator,
    generate_debug_test_names,
    generate_scenario_test_names,
)


class TestMachineCLI:
  """Test the Machine CLI."""

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="door_monitor",
              module_path="cli_machine.door_monitor.DoorMonitorCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="slack_bot",
              module_path="cli_machine.slack_bot.SlackBotCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_path="cli_machine.task_scheduler.TaskSchedulerCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="temp_monitor",
              module_path=
              "cli_machine.temperature_monitor.TemperatureMonitorCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_snapshot config.json",
              module_path="cli_machine.upload_snapshot.UploadSnapshotCommand",
              module_class_args=["config.json"]
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_video config.json",
              module_path="cli_machine.upload_video.UploadVideoCommand",
              module_class_args=["config.json"]
          ),
      ],
      ids=generate_scenario_test_names,
  )
  def test__vary_cli_command__calls_command_class(
      self,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
  ) -> None:
    scenario = cli_scenario_creator(scenario_args, machine_cli)

    scenario.invoke()

    scenario.command_mock.assert_called_once_with(
        *scenario_args.module_class_args
    )
    scenario.command_mock.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="door_monitor",
              module_path="cli_machine.door_monitor.DoorMonitorCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="slack_bot",
              module_path="cli_machine.slack_bot.SlackBotCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_path="cli_machine.task_scheduler.TaskSchedulerCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="temp_monitor",
              module_path=
              "cli_machine.temperature_monitor.TemperatureMonitorCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_snapshot config.json",
              module_path="cli_machine.upload_snapshot.UploadSnapshotCommand",
              module_class_args=["config.json"]
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_video config.json",
              module_path="cli_machine.upload_video.UploadVideoCommand",
              module_class_args=["config.json"]
          ),
      ],
      ids=generate_scenario_test_names,
  )
  @pytest.mark.parametrize(
      "debug",
      [True, False],
      ids=generate_debug_test_names,
  )
  def test__vary_cli_command__calls_loads_state(
      self,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
      debug: bool,
  ) -> None:
    scenario = cli_scenario_creator(scenario_args, machine_cli, debug)

    scenario.invoke()

    scenario.load_state_mock.assert_called_once_with(
        debug=debug,
        **scenario_args.state_args,
    )
