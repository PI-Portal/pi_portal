"""Test fixtures for the chat CLI command module tests."""
# pylint: disable=redefined-outer-name,unused-import

from typing import Callable, Type
from unittest import mock

import pytest
from pi_portal.modules.system import supervisor_config
from .. import (
    command,
    process_command,
    process_management_command,
    process_status_command,
)
from .scenarios import (
    ProcessScenario,
    TypeProcessGenericScenarioCreator,
    TypeProcessMgmtScenarioCreator,
    TypeProcessStatusScenarioCreator,
    create_generic_process_scenario_mocks,
    create_process_mgmt_scenario,
    create_process_status_scenario,
)


@pytest.fixture
def concrete_command_class() -> Type[command.ChatCommandBase]:

  class ConcreteCommand(command.ChatCommandBase):

    def invoke(self) -> None:
      raise NotImplementedError

  return ConcreteCommand


@pytest.fixture
def concrete_command_instance(
    concrete_command_class: Type[command.ChatCommandBase],
    mocked_chat_bot: mock.Mock,
) -> command.ChatCommandBase:
  return concrete_command_class(mocked_chat_bot)


@pytest.fixture
def concrete_process_command_class(
    mocked_process_invoker: mock.Mock,
) -> Type[process_command.ChatProcessCommandBase]:

  class ConcreteProcessCommand(process_command.ChatProcessCommandBase):

    process_name = supervisor_config.ProcessList.BOT

    def hook_invoker(self) -> None:
      mocked_process_invoker()

  return ConcreteProcessCommand


@pytest.fixture
def concrete_process_command_instance(
    concrete_process_command_class: (
        Type[process_command.ChatProcessCommandBase]
    ),
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> process_command.ChatProcessCommandBase:
  setup_process_command_mocks()
  return concrete_process_command_class(mocked_chat_bot)


@pytest.fixture
def concrete_process_management_command_class(
) -> Type[process_management_command.ChatProcessManagementCommandBase]:

  class ConcreteProcessManagementCommand(
      process_management_command.ChatProcessManagementCommandBase
  ):

    process_name = supervisor_config.ProcessList.BOT
    process_command = "start"

  return ConcreteProcessManagementCommand


@pytest.fixture
def concrete_process_management_command_instance(
    concrete_process_management_command_class: (
        Type[process_management_command.ChatProcessManagementCommandBase]
    ),
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> process_management_command.ChatProcessManagementCommandBase:
  setup_process_command_mocks()
  return concrete_process_management_command_class(mocked_chat_bot)


@pytest.fixture
def concrete_process_status_command_class(
) -> Type[process_status_command.ChatProcessStatusCommandBase]:

  class ConcreteProcessStatusCommand(
      process_status_command.ChatProcessStatusCommandBase
  ):

    process_name = supervisor_config.ProcessList.BOT

  return ConcreteProcessStatusCommand


@pytest.fixture
def concrete_process_status_command_instance(
    concrete_process_status_command_class: (
        Type[process_status_command.ChatProcessStatusCommandBase]
    ),
    mocked_chat_bot: mock.Mock,
    setup_process_command_mocks: Callable[[], None],
) -> process_status_command.ChatProcessStatusCommandBase:
  setup_process_command_mocks()
  return concrete_process_status_command_class(mocked_chat_bot)
