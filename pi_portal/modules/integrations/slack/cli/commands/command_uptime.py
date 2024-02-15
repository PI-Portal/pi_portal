"""Slack CLI Uptime commands."""

from pi_portal.modules.system import linux, supervisor
from .bases.command import SlackCommandBase
from .process_uptime_commands.contact_switch_monitor_uptime import (
    ContactSwitchMonitorUptimeCommand,
)
from .process_uptime_commands.slack_bot_uptime import BotUptimeCommand
from .process_uptime_commands.task_scheduler_uptime import (
    TaskSchedulerUptimeCommand,
)
from .process_uptime_commands.temp_monitor_uptime import (
    TempMonitorUptimeCommand,
)


class UptimeCommand(SlackCommandBase):
  """Slack CLI command to report the uptime of the system components.

  :param bot: The configured slack bot in use.
  """

  def invoke(self) -> None:
    """Report the uptime of the system and Pi Portal processes."""

    bot_uptime_command = BotUptimeCommand(self.slack_bot)
    switch_monitor_uptime_command = ContactSwitchMonitorUptimeCommand(
        self.slack_bot
    )
    task_scheduler_uptime_command = TaskSchedulerUptimeCommand(self.slack_bot)
    temp_monitor_uptime_command = TempMonitorUptimeCommand(self.slack_bot)

    try:
      bot_uptime_command.invoke()
      switch_monitor_uptime_command.invoke()
      task_scheduler_uptime_command.invoke()
      temp_monitor_uptime_command.invoke()
    except supervisor.SupervisorException:
      pass
    else:
      linux_uptime = linux.uptime()

      self.slack_bot.slack_client.send_message(
          f"System Uptime > {linux_uptime}\n"
          f"Bot Uptime > {bot_uptime_command.result}\n"
          "Contact Switch Monitor Uptime > "
          f"{switch_monitor_uptime_command.result}\n"
          f"Task Scheduler Uptime > {task_scheduler_uptime_command.result}\n"
          f"Temperature Monitor Uptime > {temp_monitor_uptime_command.result}"
      )
