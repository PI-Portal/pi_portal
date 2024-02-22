"""Tests for the Machine CLI."""

from unittest import mock

import pytest
from .. import cli_machine
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
              cli_command="contact_switch_monitor",
              module_class="ContactSwitchMonitorCommand",
              module_name="contact_switch_monitor",
          ),
          CliScenarioCreatorArgs(
              cli_command="slack_bot",
              module_class="SlackBotCommand",
              module_name="slack_bot",
          ),
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_class="TaskSchedulerCommand",
              module_name="task_scheduler",
          ),
          CliScenarioCreatorArgs(
              cli_command="temp_monitor",
              module_class="TemperatureMonitorCommand",
              module_name="temperature_monitor",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_snapshot config.json",
              module_class="UploadSnapshotCommand",
              module_class_args=["config.json"],
              module_name="upload_snapshot",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_video config.json",
              module_class="UploadVideoCommand",
              module_class_args=["config.json"],
              module_name="upload_video",
          ),
      ],
      ids=generate_scenario_test_names,
  )
  def test__vary_cli_command__calls_command_class(
      self,
      mocked_import_module: mock.Mock,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
  ) -> None:
    scenario = cli_scenario_creator(cli_machine, scenario_args)

    scenario.invoke()

    mocked_import_module.assert_called_once_with(
        "pi_portal.cli_commands.cli_machine." + scenario_args.module_name
    )
    scenario.command_mock.assert_called_once_with(
        *scenario_args.module_class_args
    )
    scenario.command_mock.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="contact_switch_monitor",
              module_class="ContactSwitchMonitorCommand",
              module_name="contact_switch_monitor",
          ),
          CliScenarioCreatorArgs(
              cli_command="slack_bot",
              module_class="SlackBotCommand",
              module_name="slack_bot",
          ),
          CliScenarioCreatorArgs(
              cli_command="task_scheduler",
              module_class="TaskSchedulerCommand",
              module_name="task_scheduler",
          ),
          CliScenarioCreatorArgs(
              cli_command="temp_monitor",
              module_class="TemperatureMonitorCommand",
              module_name="temperature_monitor",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_snapshot config.json",
              module_class="UploadSnapshotCommand",
              module_class_args=["config.json"],
              module_name="upload_snapshot",
          ),
          CliScenarioCreatorArgs(
              cli_command="upload_video config.json",
              module_class="UploadVideoCommand",
              module_class_args=["config.json"],
              module_name="upload_video",
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
    scenario = cli_scenario_creator(cli_machine, scenario_args, debug)

    scenario.invoke()

    scenario.load_state_mock.assert_called_once_with(
        debug=debug,
        **scenario_args.state_args,
    )
