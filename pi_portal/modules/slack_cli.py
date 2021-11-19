"""Slack CLI."""

import sys
from datetime import datetime
from typing import TYPE_CHECKING, List

import humanize
from pi_portal.modules import linux, motion, supervisor

if TYPE_CHECKING:
  from pi_portal.modules.slack import Client  # pragma: no cover


class SlackCLI:
  """The Slack Command Line Interface."""

  def __init__(self, client: "Client"):
    self.slack_client = client
    self.supervisor_client = supervisor.SupervisorClient()
    self.prefix = "command_"

  def notify_already_up(self):
    """Report that the service is already up."""

    self.slack_client.send_message("Already running ...")

  def notify_already_down(self):
    """Report that the service is already down."""

    self.slack_client.send_message("Already stopped ...")

  def notify_error(self):
    """Report that an error has occurred with supervisor."""

    self.slack_client.send_message(
        "An internal error occurred ... you better take a look."
    )

  def notify_starting(self):
    """Report that the service is starting."""

    self.slack_client.send_message("Starting ...")

  def notify_stopping(self):
    """Report that the service is stopping."""

    self.slack_client.send_message("Shutting down ...")

  def get_commands(self) -> List[str]:
    """Generate a list of valid commands.

    :return: The list of valid commands.
    """

    commands = []
    for method in dir(self):
      if method.startswith("command_") is True:
        commands.append(method)
    return commands

  def command_id(self):
    """Report the logger ID the bot is currently running with."""

    self.slack_client.send_message(f"ID: {self.slack_client.config.log_uuid}")

  def command_arm(self):
    """Arm the security system."""

    try:
      status = self.supervisor_client.status(supervisor.ProcessList.CAMERA)
      if status not in [
          supervisor.ProcessStatus.RUNNING.value,
          supervisor.ProcessStatus.RESTARTING.value,
      ]:
        self.supervisor_client.start(supervisor.ProcessList.CAMERA)
        self.notify_starting()
      else:
        self.notify_already_up()
    except supervisor.SupervisorException:
      self.notify_error()

  def command_disarm(self):
    """Disarm the security system."""

    try:
      status = self.supervisor_client.status(supervisor.ProcessList.CAMERA)
      if status in [
          supervisor.ProcessStatus.RUNNING.value,
          supervisor.ProcessStatus.RESTARTING.value,
      ]:
        self.supervisor_client.stop(supervisor.ProcessList.CAMERA)
        self.notify_stopping()
      else:
        self.notify_already_down()
    except supervisor.SupervisorException:
      self.notify_error()

  def command_help(self):
    """Report the list of valid commands."""

    commands = [
        command.replace(self.prefix, '') for command in self.get_commands()
    ]
    self.slack_client.send_message(f"Available Commands: {', '.join(commands)}")

  def command_restart(self):
    """Terminate the bot, and rely on supervisor to restart it."""

    self.slack_client.send_message("Rebooting myself ...")
    exit(0)

  def command_snapshot(self):
    """Post a realtime camera snapshot to Slack."""

    try:
      camera_status = self.supervisor_client.status(
          supervisor.ProcessList.CAMERA
      )
      if camera_status != supervisor.ProcessStatus.RUNNING.value:
        self.slack_client.send_message("You must arm the system first.")
      else:
        self.slack_client.motion_client.take_snapshot()
        self.slack_client.send_file(
            self.slack_client.motion_client.snapshot_fname
        )
    except (supervisor.SupervisorException, motion.MotionException):
      self.notify_error()

  def command_status(self):
    """Report the current status of the security system."""

    status = self.supervisor_client.status(supervisor.ProcessList.CAMERA)
    self.slack_client.send_message(f"Status: {status}")

  def command_uptime(self):
    """Report the current uptime of this bot."""
    system_uptime = linux.uptime()
    monitor_uptime = "Not Running"
    bot_uptime = "Not Running"

    try:

      status = self.supervisor_client.status(supervisor.ProcessList.MONITOR)
      if status == supervisor.ProcessStatus.RUNNING.value:
        monitor_uptime = humanize.naturaldelta(
            datetime.now() - datetime.fromtimestamp(
                int(
                    self.supervisor_client.
                    uptime(supervisor.ProcessList.MONITOR)
                )
            )
        )

      status = self.supervisor_client.status(supervisor.ProcessList.BOT)
      if status == supervisor.ProcessStatus.RUNNING.value:
        bot_uptime = humanize.naturaldelta(
            datetime.now() - datetime.fromtimestamp(
                int(self.supervisor_client.uptime(supervisor.ProcessList.BOT))
            )
        )

      self.slack_client.send_message(
          f"System Uptime > {system_uptime}\n"
          f"Monitor Uptime > {monitor_uptime}\n"
          f"Bot Uptime > {bot_uptime}"
      )

    except supervisor.SupervisorException:
      self.notify_error()
