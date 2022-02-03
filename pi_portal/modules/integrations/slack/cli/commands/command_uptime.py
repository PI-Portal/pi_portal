"""Slack CLI Uptime commands."""

from typing import TYPE_CHECKING

from pi_portal.modules.system import (
    linux,
    supervisor,
    supervisor_config,
    supervisor_process,
)
from .bases.command import SlackCommandBase
from .bases.nested_process_uptime_command import NestedSlackUptimeCommandBase

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.client import \
      SlackClient  # pragma: no cover


class UptimeCommand(SlackCommandBase):
  """Slack CLI command to report the uptime of the system components.

  :param client: The configured slack client to use.
  """

  def __init__(self, client: "SlackClient") -> None:
    super().__init__(client)
    self.bot_process = supervisor_process.SupervisorProcess(
        supervisor_config.ProcessList.BOT
    )
    self.monitor_process = supervisor_process.SupervisorProcess(
        supervisor_config.ProcessList.MONITOR
    )

  def invoke(self) -> None:
    """Report the uptime of the system and Pi Portal processes."""

    bot_uptime_command = BotUptimeCommand(self.slack_client)
    monitor_uptime_command = DoorMonitorUptimeCommand(self.slack_client)

    try:
      bot_uptime_command.invoke()
      monitor_uptime_command.invoke()
    except supervisor.SupervisorException:
      pass
    else:
      linux_uptime = linux.uptime()

      self.slack_client.send_message(
          f"System Uptime > {linux_uptime}\n"
          f"Door Monitor Uptime > {monitor_uptime_command.result}\n"
          f"Bot Uptime > {bot_uptime_command.result}"
      )


class BotUptimeCommand(NestedSlackUptimeCommandBase):
  """Retrieves uptime for the BOT process."""

  process_name = supervisor_config.ProcessList.BOT


class DoorMonitorUptimeCommand(NestedSlackUptimeCommandBase):
  """Retrieves uptime for the MONITOR process."""

  process_name = supervisor_config.ProcessList.MONITOR