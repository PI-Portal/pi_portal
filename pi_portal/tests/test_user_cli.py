"""Tests for the User CLI."""

import pytest
from ..cli_user import cli as user_cli
from .conftest import (
    CliScenarioCreatorArgs,
    TypeCliScenarioCreator,
    generate_debug_test_names,
    generate_scenario_test_names,
)


class TestUserCLI:
  """Test the User CLI."""

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="install_config config.json",
              module_class_args=["config.json", False],
              module_path="cli_user.installer.InstallerCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="install_config -y config.json",
              module_class_args=["config.json", True],
              module_path="cli_user.installer.InstallerCommand",
          ),
          CliScenarioCreatorArgs(
              cli_command="version",
              module_path="cli_user.version.VersionCommand",
          ),
      ],
      ids=generate_scenario_test_names,
  )
  def test__vary_cli_command__calls_command_class(
      self,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
  ) -> None:
    scenario = cli_scenario_creator(scenario_args, user_cli)

    scenario.invoke()

    scenario.command_mock.assert_called_once_with(
        *scenario_args.module_class_args
    )
    scenario.command_mock.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="install_config config.json",
              module_path="cli_user.installer.InstallerCommand",
              state_args={"file_path": "config.json"}
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
    scenario = cli_scenario_creator(scenario_args, user_cli, debug)

    scenario.invoke()

    scenario.load_state_mock.assert_called_once_with(
        debug=debug,
        **scenario_args.state_args,
    )

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="version",
              module_path="cli_user.version.VersionCommand",
          ),
      ],
      ids=generate_scenario_test_names,
  )
  def test__vary_cli_command__does_not_load_state(
      self,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
  ) -> None:
    scenario = cli_scenario_creator(scenario_args, user_cli)

    scenario.invoke()

    scenario.load_state_mock.assert_not_called()
