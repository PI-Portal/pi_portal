"""Test the Slack CLI Uptime Command."""

from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands import command_uptime
from pi_portal.modules.system import supervisor, supervisor_config
from ..bases.tests.fixtures import (
    command_harness,
    nested_process_uptime_command_harness,
)


class TestBotUptimeCommand(
    nested_process_uptime_command_harness.NestedUptimeCommandBaseTestHarness
):
  """Test the BotUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.BOT

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_uptime.BotUptimeCommand


class TestDoorMonitorUptimeCommand(
    nested_process_uptime_command_harness.NestedUptimeCommandBaseTestHarness
):
  """Test the DoorMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.DOOR_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_uptime.DoorMonitorUptimeCommand


class TestTempMonitorUptimeCommand(
    nested_process_uptime_command_harness.NestedUptimeCommandBaseTestHarness
):
  """Test the TempMonitorUptimeCommand class."""

  __test__ = True
  expected_process_name = supervisor_config.ProcessList.TEMP_MONITOR

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_uptime.TempMonitorUptimeCommand


class TestUptimeCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Uptime Command."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_uptime.UptimeCommand

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".TempMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke(
      self,
      m_linux: mock.Mock,
      m_temp: mock.Mock,
      m_door: mock.Mock,
      m_bot: mock.Mock,
  ) -> None:
    m_bot.return_value.result = "bot uptime"
    m_door.return_value.result = "door monitor uptime"
    m_temp.return_value.result = "temp monitor uptime"
    m_linux.return_value = "linux uptime"

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        f"System Uptime > {m_linux.return_value}\n"
        f"Door Monitor Uptime > {m_door.return_value.result}\n"
        f"Temperature Monitor Uptime > {m_temp.return_value.result}\n"
        f"Bot Uptime > {m_bot.return_value.result}"
    )

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".TempMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke_error_bot(
      self,
      _: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
      m_bot: mock.Mock,
  ) -> None:
    m_bot.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".TempMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke_error_door(
      self,
      _: mock.Mock,
      __: mock.Mock,
      m_door: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    m_door.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()

  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".TempMonitorUptimeCommand")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke_error_temp(
      self,
      _: mock.Mock,
      m_temp: mock.Mock,
      __: mock.Mock,
      ___: mock.Mock,
  ) -> None:
    m_temp.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()
