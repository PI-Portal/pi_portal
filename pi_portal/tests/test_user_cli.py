"""Tests for the User CLI."""

from unittest import mock

import pytest
from .. import cli_user
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
              module_class="InstallerCommand",
              module_class_args=["config.json", False],
              module_name="installer",
          ),
          CliScenarioCreatorArgs(
              cli_command="install_config -y config.json",
              module_class="InstallerCommand",
              module_class_args=["config.json", True],
              module_name="installer",
          ),
          CliScenarioCreatorArgs(
              cli_command="version",
              module_class="VersionCommand",
              module_name="version",
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
    scenario = cli_scenario_creator(cli_user, scenario_args)

    scenario.invoke()

    mocked_import_module.assert_called_once_with(
        "pi_portal.cli_commands.cli_user." + scenario_args.module_name
    )
    scenario.command_mock.assert_called_once_with(
        *scenario_args.module_class_args
    )
    scenario.command_mock.return_value.invoke.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_args",
      [
          CliScenarioCreatorArgs(
              cli_command="install_config config.json",
              module_class="InstallerCommand",
              module_name="installer",
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
    scenario = cli_scenario_creator(cli_user, scenario_args, debug)

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
              module_class="VersionCommand",
              module_name="version",
          ),
      ],
      ids=generate_scenario_test_names,
  )
  def test__vary_cli_command__does_not_load_state(
      self,
      scenario_args: CliScenarioCreatorArgs,
      cli_scenario_creator: TypeCliScenarioCreator,
  ) -> None:
    scenario = cli_scenario_creator(cli_user, scenario_args)

    scenario.invoke()

    scenario.load_state_mock.assert_not_called()
