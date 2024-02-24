"""Test fixtures for the chat CLI command module tests."""
# pylint: disable=redefined-outer-name,unused-import

from typing import Callable, Type
from unittest import mock

import pytest
from pi_portal.modules.system import supervisor_config
from ..process_uptime_subcommand import ChatProcessUptimeCommandBase
from .scenarios import (
    ProcessScenario,
    TypeProcessUptimeScenarioCreator,
    create_generic_process_scenario_mocks,
    create_process_uptime_scenario,
)


@pytest.fixture
def concrete_process_uptime_command_class(
) -> Type[ChatProcessUptimeCommandBase]:

  class ConcreteProcessUptimeCommand(ChatProcessUptimeCommandBase):

    process_name = supervisor_config.ProcessList.BOT

  return ConcreteProcessUptimeCommand


@pytest.fixture
def concrete_process_uptime_command_instance(
    concrete_process_uptime_command_class: Type[ChatProcessUptimeCommandBase],
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> ChatProcessUptimeCommandBase:
  setup_process_command_mocks()
  return concrete_process_uptime_command_class(mocked_chat_bot)
