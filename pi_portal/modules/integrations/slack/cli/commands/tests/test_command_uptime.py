"""Test the Slack CLI Uptime Command."""

from collections import OrderedDict
from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands import command_uptime
from pi_portal.modules.integrations.slack.cli.commands.bases import (
    process_command,
)
from pi_portal.modules.system import supervisor
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases.tests.fixtures import command_harness


class TestUptimeCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Uptime Command."""

  __test__ = True

  uptimes = OrderedDict(
      {
          "linux": "1000 days",
          "slack_bot": "1 day",
          "door_monitor": "2 days",
          "task_scheduler": "3 days",
          "temp_monitor": "4 days",
      }
  )

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_uptime.UptimeCommand

  @mock.patch(process_command.__name__ + ".SupervisorProcess")
  @mock.patch(command_uptime.__name__ + ".linux.uptime")
  def test_invoke__correct_message(
      self,
      m_linux: mock.Mock,
      m_process: mock.Mock,
  ) -> None:
    m_process.return_value.uptime.side_effect = list(self.uptimes.values())[1:]
    m_linux.return_value = self.uptimes["linux"]

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        f"System Uptime > {self.uptimes['linux']}\n"
        f"Bot Uptime > {self.uptimes['slack_bot']}\n"
        f"Door Monitor Uptime > {self.uptimes['door_monitor']}\n"
        f"Task Scheduler Uptime > {self.uptimes['task_scheduler']}\n"
        f"Temperature Monitor Uptime > {self.uptimes['temp_monitor']}"
    )

  @mock.patch(process_command.__name__ + ".SupervisorProcess")
  @mock.patch(command_uptime.__name__ + ".linux.uptime", mock.Mock())
  def test_invoke__correct_processes(
      self,
      m_process: mock.Mock,
  ) -> None:
    self.instance.invoke()
    m_process.return_value.uptime.return_value = "string"

    assert len(m_process.mock_calls) == 12
    assert m_process.mock_calls[0:4] == [
        mock.call(ProcessList.BOT),
        mock.call(ProcessList.DOOR_MONITOR),
        mock.call(ProcessList.TASK_SCHEDULER),
        mock.call(ProcessList.TEMP_MONITOR),
    ]
    assert m_process.mock_calls[4:8] == [mock.call().uptime()] * 4
    assert [str(call) for call in m_process.mock_calls[8:12]] == \
           ["call().uptime().__str__()"] * 4

  @mock.patch(process_command.__name__ + ".SupervisorProcess", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".linux.uptime", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".BotUptimeCommand")
  def test_invoke__error_bot(
      self,
      m_bot: mock.Mock,
  ) -> None:
    m_bot.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()

  @mock.patch(process_command.__name__ + ".SupervisorProcess", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".linux.uptime", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".DoorMonitorUptimeCommand")
  def test_invoke__error_door(
      self,
      m_door: mock.Mock,
  ) -> None:
    m_door.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()

  @mock.patch(process_command.__name__ + ".SupervisorProcess", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".linux.uptime", mock.Mock())
  @mock.patch(command_uptime.__name__ + ".TempMonitorUptimeCommand")
  def test_invoke__error_temp(
      self,
      m_temp: mock.Mock,
  ) -> None:
    m_temp.return_value.invoke.side_effect = supervisor.SupervisorException(
        "Boom!"
    )

    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_not_called()
