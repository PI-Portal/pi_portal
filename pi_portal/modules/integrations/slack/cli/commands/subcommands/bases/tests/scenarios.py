"""Scenario test fixtures for the chat CLI command module tests."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, NamedTuple
from unittest import mock

import pytest
from pi_portal.modules.integrations.slack.cli.commands.bases.tests import \
    scenarios as base_scenarios
from typing_extensions import TypeAlias
from ..process_uptime_subcommand import ChatProcessUptimeCommandBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable

ProcessScenario = base_scenarios.ProcessScenario
create_generic_process_scenario_mocks = (
    base_scenarios.create_generic_process_scenario_mocks
)

TypeProcessUptimeScenarioCreator: TypeAlias = (
    "Callable[[base_scenarios.ProcessScenario], ProcessUptimeScenarioMocks]"
)


class ProcessUptimeScenarioMocks(NamedTuple):
  command_instance: ChatProcessUptimeCommandBase
  process_command_mock: mock.Mock
  notifier_mock: mock.Mock


@pytest.fixture
def create_process_uptime_scenario(
    concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
    create_generic_process_scenario_mocks: (
        base_scenarios.TypeProcessGenericScenarioCreator
    ),
) -> "TypeProcessUptimeScenarioCreator":

  def create(
      scenario: base_scenarios.ProcessScenario
  ) -> "ProcessUptimeScenarioMocks":
    created_scenario = create_generic_process_scenario_mocks(
        scenario,
        concrete_process_uptime_command_instance,
    )
    return ProcessUptimeScenarioMocks(
        command_instance=concrete_process_uptime_command_instance,
        process_command_mock=created_scenario.process_command_mock,
        notifier_mock=created_scenario.notifier_mock,
    )

  return create
