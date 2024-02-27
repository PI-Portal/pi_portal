"""Chat CLI Uptime commands."""

from pi_portal.modules.system import linux
from .bases.command import ChatCommandBase
from .subcommands.uptime_chat_bot import BotUptimeCommand
from .subcommands.uptime_contact_switch_monitor import (
    ContactSwitchMonitorUptimeCommand,
)
from .subcommands.uptime_task_scheduler import TaskSchedulerUptimeCommand
from .subcommands.uptime_temp_monitor import TempMonitorUptimeCommand


class UptimeCommand(ChatCommandBase):
  """Chat CLI command to report the uptime of the system components."""

  exception_message = "An error occurred when collecting uptime information..."

  def invoke(self) -> None:
    """Report the uptime of the system and Pi Portal processes."""

    bot_uptime_command = BotUptimeCommand(self.chatbot)
    switch_monitor_uptime_command = ContactSwitchMonitorUptimeCommand(
        self.chatbot
    )
    task_scheduler_uptime_command = TaskSchedulerUptimeCommand(self.chatbot)
    temp_monitor_uptime_command = TempMonitorUptimeCommand(self.chatbot)

    try:
      linux_uptime = linux.uptime()
      bot_uptime_command.invoke()
      switch_monitor_uptime_command.invoke()
      task_scheduler_uptime_command.invoke()
      temp_monitor_uptime_command.invoke()
    except Exception:  # pylint: disable=broad-exception-caught
      self.notifier.notify_error()
    else:
      self.chatbot.task_scheduler_client.chat_send_message(
          f"System Uptime > {linux_uptime}\n"
          f"Bot Uptime > {bot_uptime_command.result}\n"
          "Contact Switch Monitor Uptime > "
          f"{switch_monitor_uptime_command.result}\n"
          f"Task Scheduler Uptime > {task_scheduler_uptime_command.result}\n"
          f"Temperature Monitor Uptime > {temp_monitor_uptime_command.result}"
      )
