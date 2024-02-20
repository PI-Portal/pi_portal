"""Test the UptimeCommand class."""

from typing import Dict, List
from unittest import mock

import pytest
from pi_portal.modules.integrations.slack.cli.commands import UptimeCommand
from ..bases import command


class TestUptimeCommand:
  """Test the UptimeCommand class."""

  def test_initialize__inheritance(
      self,
      uptime_command_instance: UptimeCommand,
  ) -> None:
    assert isinstance(
        uptime_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__no_error__calls_expected_processes(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_linux_module: mock.Mock,
      mocked_uptime_subcommands: Dict[str, mock.Mock],
  ) -> None:

    uptime_command_instance.invoke()

    mocked_linux_module.uptime.assert_called_once_with()
    for mocked_class in mocked_uptime_subcommands.values():
      mocked_class.return_value.invoke.assert_called_once_with()

  def test_invoke__no_error__sends_correct_message(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_linux_module: mock.Mock,
      mocked_chat_bot: mock.Mock,
      mocked_uptime_subcommands: Dict[str, mock.Mock],
  ) -> None:
    uptime_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "System Uptime > "
        f"{mocked_linux_module.uptime.return_value}\n"
        "Bot Uptime > " +
        str(mocked_uptime_subcommands['BotUptimeCommand'].return_value.result) +
        "\n"
        "Contact Switch Monitor Uptime > " + str(
            mocked_uptime_subcommands['ContactSwitchMonitorUptimeCommand'].
            return_value.result
        ) + "\n"
        "Task Scheduler Uptime > " + str(
            mocked_uptime_subcommands['TaskSchedulerUptimeCommand'].
            return_value.result
        ) + "\n"
        "Temperature Monitor Uptime > " + str(
            mocked_uptime_subcommands['TempMonitorUptimeCommand'].return_value.
            result
        )
    )

  def test_invoke__linux_uptime_error__calls_expected_processes(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_linux_module: mock.Mock,
      mocked_uptime_subcommands: Dict[str, mock.Mock],
  ) -> None:
    mocked_linux_module.uptime.side_effect = Exception

    uptime_command_instance.invoke()

    for mocked_class in mocked_uptime_subcommands.values():
      mocked_class.return_value.uptime.assert_not_called()

  def test_invoke__linux_uptime_error__sends_error_message(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_chat_bot: mock.Mock,
      mocked_cli_notifier: mock.Mock,
      mocked_linux_module: mock.Mock,
  ) -> None:
    mocked_linux_module.uptime.side_effect = Exception

    uptime_command_instance.invoke()

    mocked_cli_notifier.return_value.notify_error.assert_called_once_with()
    mocked_chat_bot.chat_client.send_message.assert_not_called()

  @pytest.mark.parametrize(
      "error_class,expected_calls", [
          ["BotUptimeCommand", [True, False, False, False]],
          ["ContactSwitchMonitorUptimeCommand", [True, True, False, False]],
          ["TaskSchedulerUptimeCommand", [True, True, True, False]],
          ["TempMonitorUptimeCommand", [True, True, True, True]],
      ]
  )
  def test_invoke__vary_uptime_error__calls_expected_processes(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_uptime_subcommands: Dict[str, mock.Mock],
      error_class: str,
      expected_calls: List[bool],
  ) -> None:
    mocked_uptime_subcommands[error_class].return_value.invoke.side_effect = (
        Exception
    )

    uptime_command_instance.invoke()

    for index, mocked_class in enumerate(mocked_uptime_subcommands.values()):
      called = mocked_class.return_value.invoke.mock_calls == [mock.call()]
      assert called == expected_calls[index]

  @pytest.mark.parametrize(
      "error_class", [
          "BotUptimeCommand",
          "ContactSwitchMonitorUptimeCommand",
          "TaskSchedulerUptimeCommand",
          "TempMonitorUptimeCommand",
      ]
  )
  def test_invoke__vary_uptime_error__sends_error_message(
      self,
      uptime_command_instance: UptimeCommand,
      mocked_chat_bot: mock.Mock,
      mocked_cli_notifier: mock.Mock,
      mocked_uptime_subcommands: Dict[str, mock.Mock],
      error_class: str,
  ) -> None:
    mocked_uptime_subcommands[error_class].return_value.invoke.side_effect = (
        Exception
    )

    uptime_command_instance.invoke()

    mocked_cli_notifier.return_value.notify_error.assert_called_once_with()
    mocked_chat_bot.chat_client.send_message.assert_not_called()
