"""Test the ChatProcessUptimeCommandBase class."""
from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.cli.commands.bases import (
    command,
    process_command,
    process_status_command,
)
from pi_portal.modules.system import supervisor, supervisor_config
from ..process_uptime_subcommand import ChatProcessUptimeCommandBase
from .conftest import ProcessScenario, TypeProcessUptimeScenarioCreator


class TestChatProcessUptimeCommandBase:
  """Test the ChatProcessUptimeCommandBase class."""

  def test_initialize__attributes(
      self,
      concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
  ) -> None:
    assert concrete_process_uptime_command_instance.process_name == (
        supervisor_config.ProcessList.BOT
    )

  def test_initialize__inheritance(
      self,
      concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
  ) -> None:
    assert isinstance(
        concrete_process_uptime_command_instance,
        command.ChatCommandBase,
    )
    assert isinstance(
        concrete_process_uptime_command_instance,
        process_command.ChatProcessCommandBase,
    )
    assert isinstance(
        concrete_process_uptime_command_instance,
        process_status_command.ChatProcessStatusCommandBase,
    )

  def test_initialize__bot(
      self,
      concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert concrete_process_uptime_command_instance.chatbot == (mocked_chat_bot)

  def test_initialize__notifier(
      self,
      concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
      mocked_cli_notifier: mock.Mock,
      mocked_task_scheduler_client: mock.Mock,
  ) -> None:
    assert concrete_process_uptime_command_instance.notifier == (
        mocked_cli_notifier.return_value
    )
    mocked_cli_notifier.assert_called_once_with(mocked_task_scheduler_client)

  def test_initialize__supervisor_process(
      self,
      concrete_process_uptime_command_instance: ChatProcessUptimeCommandBase,
      mocked_supervisor_process: mock.Mock,
  ) -> None:
    assert concrete_process_uptime_command_instance.process == (
        mocked_supervisor_process.return_value
    )
    mocked_supervisor_process.assert_called_once_with(
        concrete_process_uptime_command_instance.process_name
    )

  @pytest.mark.parametrize("scenario", [ProcessScenario(command="uptime")])
  def test_invoke__calls_supervisor_process_method(
      self,
      create_process_uptime_scenario: TypeProcessUptimeScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_uptime_scenario(scenario)

    created_scenario.command_instance.invoke()

    created_scenario.process_command_mock.assert_called_once_with()

  @pytest.mark.parametrize("scenario", [ProcessScenario(command="uptime")])
  def test_invoke__sets_correct_result_value(
      self,
      create_process_uptime_scenario: TypeProcessUptimeScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_uptime_scenario(scenario)

    created_scenario.command_instance.invoke()

    assert created_scenario.command_instance.result == (
        created_scenario.process_command_mock.return_value
    )

  @pytest.mark.parametrize("scenario", [ProcessScenario(command="uptime")])
  def test_invoke__supervisor_exception__raises_exception(
      self,
      create_process_uptime_scenario: TypeProcessUptimeScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_uptime_scenario(scenario)
    created_scenario.process_command_mock.side_effect = (
        supervisor.SupervisorException
    )

    with pytest.raises(supervisor.SupervisorException) as exc:
      created_scenario.command_instance.invoke()

    assert str(
        exc.value
    ) == created_scenario.command_instance.supervisor_exception_message

  @pytest.mark.parametrize(
      "scenario",
      [ProcessScenario(
          command="uptime",
          notifier_method="notify_error",
      )]
  )
  def test_invoke__supervisor_exception__calls_notifier_method(
      self,
      create_process_uptime_scenario: TypeProcessUptimeScenarioCreator,
      scenario: ProcessScenario,
  ) -> None:
    created_scenario = create_process_uptime_scenario(scenario)
    created_scenario.process_command_mock.side_effect = (
        supervisor.SupervisorException
    )

    with pytest.raises(supervisor.SupervisorException):
      created_scenario.command_instance.invoke()

    created_scenario.notifier_mock.assert_called_once_with()
