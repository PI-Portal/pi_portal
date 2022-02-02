"""Test the Slack CLI Uptime Command."""

from typing import Type
from unittest import mock

from pi_portal.modules.integrations.slack_cli.commands import command_uptime
from pi_portal.modules.system import supervisor, supervisor_config
from ..bases.tests.fixtures import (
    command_harness,
    process_nested_uptime_command_harness,
)


class TestBotUptimeCommand(
    process_nested_uptime_command_harness.NestedUptimeCommandBaseTestHarness
):
  """Test the BotUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.BOT

  def get_test_class(self) -> Type[command_uptime.BotUptimeCommand]:
    return command_uptime.BotUptimeCommand


class DoorMonitorUptimeCommand(
    process_nested_uptime_command_harness.NestedUptimeCommandBaseTestHarness
):
  """Test the DoorMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.MONITOR

  def get_test_class(self) -> Type[command_uptime.DoorMonitorUptimeCommand]:
    return command_uptime.DoorMonitorUptimeCommand


class TestUptimeCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Uptime Command."""

  __test__ = True

  def get_test_class(self) -> Type[command_uptime.UptimeCommand]:
    return command_uptime.UptimeCommand

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke(
      self, m_linux: mock.Mock, m_door: mock.Mock, m_bot: mock.Mock
  ) -> None:
    m_bot.return_value.result = "bot uptime"
    m_door.return_value.result = "door monitor uptime"
    m_linux.return_value = "linux uptime"

    self.instance.invoke()

    self.mock_slack_client.send_message.assert_called_once_with(
        f"System Uptime > {m_linux.return_value}\n"
        f"Door Monitor Uptime > {m_door.return_value.result}\n"
        f"Bot Uptime > {m_bot.return_value.result}"
    )

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke_error_bot(
      self, m_linux: mock.Mock, m_door: mock.Mock, m_bot: mock.Mock
  ) -> None:
    m_bot.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    m_bot.return_value.result = "bot uptime"
    m_door.return_value.result = "door monitor uptime"
    m_linux.return_value = "linux uptime"

    self.instance.invoke()
    self.mock_slack_client.send_message.assert_not_called()

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke_error_door(
      self, m_linux: mock.Mock, m_door: mock.Mock, m_bot: mock.Mock
  ) -> None:
    m_door.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    m_bot.return_value.result = "bot uptime"
    m_door.return_value.result = "door monitor uptime"
    m_linux.return_value = "linux uptime"

    self.instance.invoke()
    self.mock_slack_client.send_message.assert_not_called()
