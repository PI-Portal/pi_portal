"""Test the ChatProcessManagementCommandBase class."""

from unittest import mock

import pytest
from pi_portal.modules.system import (
    supervisor,
    supervisor_config,
    supervisor_process,
)
from .. import command, process_command
from ..process_management_command import ChatProcessManagementCommandBase
from .conftest import ProcessScenario, TypeProcessMgmtScenarioCreator


class TestChatProcessManagementCommandBase:
  """Test the ChatProcessManagementCommandBase class."""

  def test_initialize__attributes(
      self,
      concrete_process_management_command_instance:
      ChatProcessManagementCommandBase,
  ) -> None:
    assert concrete_process_management_command_instance.process_name == (
        supervisor_config.ProcessList.BOT
    )

  def test_initialize__inheritance(
      self,
      concrete_process_management_command_instance:
      ChatProcessManagementCommandBase,
  ) -> None:
    assert isinstance(
        concrete_process_management_command_instance,
        command.ChatCommandBase,
    )
    assert isinstance(
        concrete_process_management_command_instance,
        process_command.ChatProcessCommandBase,
    )

  def test_initialize__bot(
      self,
      concrete_process_management_command_instance:
      ChatProcessManagementCommandBase,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert concrete_process_management_command_instance.chatbot == (
        mocked_chat_bot
    )

  def test_initialize__notifier(
      self,
      concrete_process_management_command_instance:
      ChatProcessManagementCommandBase,
      mocked_chat_client: mock.Mock,
      mocked_cli_notifier: mock.Mock,
  ) -> None:
    assert concrete_process_management_command_instance.notifier == (
        mocked_cli_notifier.return_value
    )
    mocked_cli_notifier.assert_called_once_with(mocked_chat_client)

  def test_initialize__supervisor_process(
      self,
      concrete_process_management_command_instance:
      ChatProcessManagementCommandBase,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert concrete_process_management_command_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        concrete_process_management_command_instance.process_name
    )

  @pytest.mark.parametrize(
      "scenario", [
          ProcessScenario(command="start"),
          ProcessScenario(command="stop"),
      ]
  )
  def test_invoke__calls_supervisor_process_method(
      self,
      create_process_mgmt_scenario: TypeProcessMgmtScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_mgmt_scenario(scenario)

    created_scenario.command_instance.invoke()

    created_scenario.process_command_mock.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario", [
          ProcessScenario(
              command="start",
              notifier_method="notify_start",
          ),
          ProcessScenario(
              command="stop",
              notifier_method="notify_stop",
          )
      ]
  )
  def test_invoke__calls_notifier_method(
      self,
      create_process_mgmt_scenario: TypeProcessMgmtScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_mgmt_scenario(scenario)

    created_scenario.command_instance.invoke()

    created_scenario.notifier_mock.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario", [
          ProcessScenario(
              command="start",
              notifier_method="notify_error",
          ),
          ProcessScenario(
              command="stop",
              notifier_method="notify_error",
          )
      ]
  )
  def test_invoke__supervisor_exception__calls_notifier_method(
      self,
      create_process_mgmt_scenario: TypeProcessMgmtScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_mgmt_scenario(scenario)
    created_scenario.process_command_mock.side_effect = (
        supervisor.SupervisorException
    )

    created_scenario.command_instance.invoke()

    created_scenario.notifier_mock.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario", [
          ProcessScenario(
              command="start",
              notifier_method="notify_already_start",
          ),
          ProcessScenario(
              command="stop",
              notifier_method="notify_already_stop",
          )
      ]
  )
  def test_invoke__supervisor_process_exception__calls_notifier_method(
      self,
      create_process_mgmt_scenario: TypeProcessMgmtScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_mgmt_scenario(scenario)
    created_scenario.process_command_mock.side_effect = (
        supervisor_process.SupervisorProcessException
    )

    created_scenario.command_instance.invoke()

    created_scenario.notifier_mock.assert_called_once_with()
