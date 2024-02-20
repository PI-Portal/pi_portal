"""Chat CLI command handler."""

from typing import TYPE_CHECKING, Type

from pi_portal.modules.integrations.slack.cli import commands
from pi_portal.modules.integrations.slack.cli.commands.bases.command import (
    ChatCommandBase,
)

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.bot import \
      SlackBot  # pragma: no cover


class ChatCLICommandHandler:
  """Chat CLI command handler.

  :param bot: The configured chatbot in use.
  """

  method_prefix = "command_"

  def __init__(self, bot: "SlackBot") -> None:
    self.chatbot = bot

  def handle(self, command_class: Type[ChatCommandBase]) -> None:
    """Handle a command class instance.

    :param command_class:  The command class to invoke.
    """
    instance = command_class(self.chatbot)
    instance.invoke()

  def command_id(self) -> None:
    """Report the logger ID the bot is currently running with."""

    self.handle(commands.IDCommand)

  def command_arm(self) -> None:
    """Arm the security system."""

    self.handle(commands.ArmCommand)

  def command_disarm(self) -> None:
    """Disarm the security system."""

    self.handle(commands.DisarmCommand)

  def command_help(self) -> None:
    """Report the list of valid commands."""

    self.handle(commands.HelpCommand)

  def command_restart(self) -> None:
    """Terminate the bot, and rely on supervisor to restart it."""

    self.handle(commands.RestartCommand)

  def command_snapshot(self) -> None:
    """Post a realtime camera snapshot to chat."""

    self.handle(commands.SnapshotCommand)

  def command_status(self) -> None:
    """Report the current status of the security system."""

    self.handle(commands.StatusCommand)

  def command_temp(self) -> None:
    """Report the current temperature from polling the sensors."""

    self.handle(commands.TemperatureCommand)

  def command_uptime(self) -> None:
    """Report the current uptime of this bot."""

    self.handle(commands.UptimeCommand)
