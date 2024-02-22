"""Test fixtures for the CLI tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from types import ModuleType
from typing import Any, Callable, Dict, List, NamedTuple, Protocol
from unittest import mock

import pytest
from click.testing import CliRunner


class TypeCliScenarioCreator(Protocol):

  def __call__(
      self,
      cli_module: ModuleType,
      scenario: "CliScenarioCreatorArgs",
      debug: bool = False
  ) -> "CliScenario":
    ...


class CliScenarioCreatorArgs(NamedTuple):
  cli_command: str
  module_name: str
  module_class: str
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
def mocked_import_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def cli_runner() -> CliRunner:
  return CliRunner()


@pytest.fixture
def cli_scenario_creator(
    cli_runner: CliRunner,
    mocked_import_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> TypeCliScenarioCreator:

  def creator(
      cli_module: ModuleType,
      scenario: CliScenarioCreatorArgs,
      debug: bool = False,
  ) -> CliScenario:
    command_mock = mock.Mock()
    load_state_mock = command_mock.return_value.load_state
    mocked_import_module.return_value.attach_mock(
        command_mock,
        scenario.module_class,
    )

    monkeypatch.setattr(
        cli_module.__name__ + ".import_module",
        mocked_import_module,
    )

    def invoke() -> None:
      command_prefix = "--debug " if debug else ""
      cli_runner.invoke(
          cli_module.cli,
          command_prefix + scenario.cli_command,
      )

    return CliScenario(
        invoke=invoke,
        command_mock=command_mock,
        load_state_mock=load_state_mock,
    )

  return creator
