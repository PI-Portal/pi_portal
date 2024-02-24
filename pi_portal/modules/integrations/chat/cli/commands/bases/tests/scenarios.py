"""Scenario test fixtures for the chat CLI command module tests."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, NamedTuple, Optional, TypeVar
from unittest import mock

import pytest
from typing_extensions import TypeAlias
from .. import (
    process_command,
    process_management_command,
    process_status_command,
)

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable

TypeProcessGenericScenarioCreator: TypeAlias = (
    "Callable[[ProcessScenario, process_command.ChatProcessCommandBase], "
    "ProcessScenarioMocksGeneric]"
)
TypeProcessMgmtScenarioCreator: TypeAlias = (
    "Callable[[ProcessScenario], ProcessManagementScenarioMocks]"
)
TypeProcessStatusScenarioCreator: TypeAlias = (
    "Callable[[ProcessScenario], ProcessStatusScenarioMocks]"
)


class ProcessScenario(NamedTuple):
  command: str
  notifier_method: Optional[str] = None


TypeConcreteProcessCommand = TypeVar(
    "TypeConcreteProcessCommand",
    bound=process_command.ChatProcessCommandBase,
)


class ProcessScenarioMocksGeneric(
    NamedTuple,
):
  process_command_mock: mock.Mock
  notifier_mock: mock.Mock


class ProcessManagementScenarioMocks(NamedTuple):
  command_instance: (
      process_management_command.ChatProcessManagementCommandBase
  )
  process_command_mock: mock.Mock
  notifier_mock: mock.Mock


class ProcessStatusScenarioMocks(NamedTuple):
  command_instance: process_status_command.ChatProcessStatusCommandBase
  process_command_mock: mock.Mock
  notifier_mock: mock.Mock


@pytest.fixture
def create_generic_process_scenario_mocks(
    mocked_cli_notifier: mock.Mock,
    mocked_supervisor_process: mock.Mock,
) -> TypeProcessGenericScenarioCreator:

  def creator(
      scenario: ProcessScenario,
      command_instance: process_command.ChatProcessCommandBase,
  ) -> ProcessScenarioMocksGeneric:
    setattr(
        command_instance,
        "process_command",
        scenario.command,
    )
    process_command_mock = getattr(
        mocked_supervisor_process.return_value,
        scenario.command,
    )
    notifier_mock = mocked_cli_notifier.return_value
    if scenario.notifier_method:
      notifier_mock = getattr(
          mocked_cli_notifier.return_value,
          scenario.notifier_method,
      )
    return ProcessScenarioMocksGeneric(
        process_command_mock=process_command_mock,
        notifier_mock=notifier_mock,
    )

  return creator


@pytest.fixture
def create_process_mgmt_scenario(
    concrete_process_management_command_instance: process_management_command.
    ChatProcessManagementCommandBase,
    create_generic_process_scenario_mocks: TypeProcessGenericScenarioCreator,
) -> "TypeProcessMgmtScenarioCreator":

  def create(scenario: ProcessScenario) -> "ProcessManagementScenarioMocks":
    created_scenario = create_generic_process_scenario_mocks(
        scenario,
        concrete_process_management_command_instance,
    )
    return ProcessManagementScenarioMocks(
        command_instance=concrete_process_management_command_instance,
        process_command_mock=created_scenario.process_command_mock,
        notifier_mock=created_scenario.notifier_mock,
    )

  return create


@pytest.fixture
def create_process_status_scenario(
    concrete_process_status_command_instance: process_status_command.
    ChatProcessStatusCommandBase,
    create_generic_process_scenario_mocks: TypeProcessGenericScenarioCreator,
) -> "TypeProcessStatusScenarioCreator":

  def create(scenario: ProcessScenario) -> "ProcessStatusScenarioMocks":
    created_scenario = create_generic_process_scenario_mocks(
        scenario,
        concrete_process_status_command_instance,
    )
    return ProcessStatusScenarioMocks(
        command_instance=concrete_process_status_command_instance,
        process_command_mock=created_scenario.process_command_mock,
        notifier_mock=created_scenario.notifier_mock,
    )

  return create
