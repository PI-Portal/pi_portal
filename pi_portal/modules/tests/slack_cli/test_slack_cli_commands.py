"""Test Slack CLI Class command methods."""

from unittest import mock

from freezegun import freeze_time
from pi_portal.modules import slack_cli, supervisor
from pi_portal.modules.tests.slack_cli.fixtures.harness import (
  TestSlackCLIHarness,
)


class TestSlackCLI(TestSlackCLIHarness):
  """Test the SlackCLI class command methods."""

  __test__ = True

  def test_get_commands(self):
    expected_commands = [
        'command_arm', 'command_disarm', 'command_help', 'command_id',
        'command_restart', 'command_snapshot', 'command_status',
        'command_uptime'
    ]
    self.assertListEqual(expected_commands, self.cli.get_commands())

  def test_command_id(self):
    self.cli.command_id()
    self.cli.slack_client.send_message.assert_called_once_with(
        f"ID: {self.cli.slack_client.config.log_uuid}"
    )

  def test_command_arm_not_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.STOPPED.value
    )
    self.cli.command_arm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.start.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.slack_client.send_message.assert_called_once_with("Starting ...")

  def test_command_arm_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.command_arm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.start.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Already running ..."
    )

  def test_command_arm_exception(self):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.SupervisorException("Boom!")
    )
    self.cli.command_arm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.start.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_command_disarm_not_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.STOPPED.value
    )
    self.cli.command_disarm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.stop.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Already stopped ..."
    )

  def test_command_disarm_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.command_disarm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.stop.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.slack_client.send_message.assert_called_once_with(
        "Shutting down ..."
    )

  def test_command_disarm_exception(self):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.SupervisorException("Boom!")
    )
    self.cli.command_disarm()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.supervisor_client.stop.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_command_help(self):
    self.cli.command_help()
    commands = [
        command.replace(self.cli.prefix, '')
        for command in self.cli.get_commands()
    ]
    self.cli.slack_client.send_message.assert_called_once_with(
        f"Available Commands: {', '.join(commands)}"
    )

  def test_command_restart(self):
    with self.assertRaises(SystemExit):
      self.cli.command_restart()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Rebooting myself ..."
    )

  def test_command_snapshot_not_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.STOPPED.value
    )
    self.cli.command_snapshot()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.slack_client.motion_client.take_snapshot.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "You must arm the system first."
    )

  def test_command_snapshot_running(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.command_snapshot()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.slack_client.motion_client.take_snapshot.assert_called_once_with()
    self.cli.slack_client.send_file.assert_called_once_with(
        self.cli.slack_client.motion_client.snapshot_fname
    )

  def test_command_snapshot_exception(self):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.SupervisorException("Boom!")
    )
    self.cli.command_snapshot()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.CAMERA
    )
    self.cli.slack_client.motion_client.take_snapshot.assert_not_called()
    self.cli.slack_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_command_status(self):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.command_status()
    self.cli.slack_client.send_message.assert_called_once_with(
        f"Status: {supervisor.ProcessStatus.RUNNING.value}"
    )

  @mock.patch(slack_cli.__name__ + ".linux.uptime")
  def test_command_uptime_not_running(self, m_linux_uptime):
    self.cli.supervisor_client.status.return_value = (
        supervisor.ProcessStatus.STOPPED.value
    )
    m_linux_uptime.return_value = "15 hours"
    self.cli.command_uptime()
    self.cli.slack_client.send_message.assert_called_once_with(
        'System Uptime > 15 hours\n'
        'Monitor Uptime > Not Running\n'
        'Bot Uptime > Not Running'
    )

  @freeze_time("2021-11-18-22:30:00")
  @mock.patch(slack_cli.__name__ + ".linux.uptime")
  def test_command_uptime_app_running(self, m_linux_uptime):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.ProcessStatus.RUNNING.value,
        supervisor.ProcessStatus.STOPPED.value
    )
    self.cli.supervisor_client.uptime.return_value = "1637290560"
    m_linux_uptime.return_value = "15 hours"
    self.cli.command_uptime()
    self.cli.slack_client.send_message.assert_called_once_with(
        'System Uptime > 15 hours\n'
        'Monitor Uptime > 4 hours\n'
        'Bot Uptime > Not Running'
    )

  @freeze_time("2021-11-18-22:30:00")
  @mock.patch(slack_cli.__name__ + ".linux.uptime")
  def test_command_uptime_bot_running(self, m_linux_uptime):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.ProcessStatus.STOPPED.value,
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.supervisor_client.uptime.return_value = "1637288711"
    m_linux_uptime.return_value = "15 hours"
    self.cli.command_uptime()
    self.cli.slack_client.send_message.assert_called_once_with(
        'System Uptime > 15 hours\n'
        'Monitor Uptime > Not Running\n'
        'Bot Uptime > 3 hours'
    )

  @freeze_time("2021-11-18-22:30:00")
  @mock.patch(slack_cli.__name__ + ".linux.uptime")
  def test_command_uptime_both_running(self, m_linux_uptime):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.ProcessStatus.RUNNING.value,
        supervisor.ProcessStatus.RUNNING.value
    )
    self.cli.supervisor_client.uptime.return_value = "1637288711"
    m_linux_uptime.return_value = "15 hours"
    self.cli.command_uptime()
    self.cli.slack_client.send_message.assert_called_once_with(
        'System Uptime > 15 hours\n'
        'Monitor Uptime > 3 hours\n'
        'Bot Uptime > 3 hours'
    )

  def test_command_uptime_exception(self):
    self.cli.supervisor_client.status.side_effect = (
        supervisor.SupervisorException("Boom!")
    )
    self.cli.command_uptime()
    self.cli.supervisor_client.status.assert_called_once_with(
        supervisor.ProcessList.MONITOR
    )
    self.cli.slack_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )
