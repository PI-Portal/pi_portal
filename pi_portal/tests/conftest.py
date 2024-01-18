"""Test fixtures for the CLI tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from typing import Callable, NamedTuple, Optional
from unittest import mock

import click
import pytest
from click.testing import CliRunner
from typing_extensions import TypeAlias

TypeMachineCliScenarioCreator: TypeAlias = \
  "Callable[[CliScenarioCreatorArgs, click.Group], CliScenario]"


class CliScenarioCreatorArgs(NamedTuple):
  cli_command: str
  module_path: str
  debug: Optional[bool] = None


class CliScenario(NamedTuple):
  invoke: Callable[[], None]
  command_mock: mock.Mock
  load_state_mock: mock.Mock
  debug: Optional[bool] = None


@pytest.fixture
def cli_runner() -> CliRunner:
  return CliRunner()


@pytest.fixture
def machine_cli_scenario_creator(
    cli_runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> TypeMachineCliScenarioCreator:

  def creator(
      scenario: CliScenarioCreatorArgs, cli_target: click.Group
  ) -> CliScenario:
    command_mock = mock.Mock()
    load_state_mock = command_mock.return_value.load_state

    monkeypatch.setattr(
        f"pi_portal.cli_commands.{scenario.module_path}",
        command_mock,
    )

    def invoke() -> None:
      command_prefix = "--debug " if scenario.debug else ""
      cli_runner.invoke(cli_target, command_prefix + scenario.cli_command)

    return CliScenario(
        invoke=invoke,
        command_mock=command_mock,
        load_state_mock=load_state_mock,
        debug=scenario.debug,
    )

  return creator
