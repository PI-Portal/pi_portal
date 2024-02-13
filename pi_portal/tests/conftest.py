"""Test fixtures for the CLI tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from typing import Any, Callable, Dict, List, NamedTuple, Protocol
from unittest import mock

import click
import pytest
from click.testing import CliRunner


class TypeCliScenarioCreator(Protocol):

  def __call__(
      self,
      scenario: "CliScenarioCreatorArgs",
      cli_target: click.Group,
      debug: bool = False
  ) -> "CliScenario":
    ...


class CliScenarioCreatorArgs(NamedTuple):
  cli_command: str
  module_path: str
  module_class_args: List[Any] = []
  state_args: Dict[str, Any] = {}


class CliScenario(NamedTuple):
  invoke: Callable[[], None]
  command_mock: mock.Mock
  load_state_mock: mock.Mock


def generate_scenario_test_names(scenario_args: CliScenarioCreatorArgs) -> str:
  return scenario_args.cli_command


def generate_debug_test_names(debug: bool) -> str:
  return f"debug {debug}"


@pytest.fixture
def cli_runner() -> CliRunner:
  return CliRunner()


@pytest.fixture
def cli_scenario_creator(
    cli_runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> TypeCliScenarioCreator:

  def creator(
      scenario: CliScenarioCreatorArgs,
      cli_target: click.Group,
      debug: bool = False,
  ) -> CliScenario:
    command_mock = mock.Mock()
    load_state_mock = command_mock.return_value.load_state

    monkeypatch.setattr(
        f"pi_portal.cli_commands.{scenario.module_path}",
        command_mock,
    )

    def invoke() -> None:
      command_prefix = "--debug " if debug else ""
      cli_runner.invoke(
          cli_target,
          command_prefix + scenario.cli_command,
      )

    return CliScenario(
        invoke=invoke,
        command_mock=command_mock,
        load_state_mock=load_state_mock,
    )

  return creator
