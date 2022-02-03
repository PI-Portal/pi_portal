"""Slack CLI command handler."""

from typing import TYPE_CHECKING, Type

from pi_portal.modules.integrations.slack.cli import commands
from pi_portal.modules.integrations.slack.cli.commands.bases.command import (
    SlackCommandBase,
)

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import \
      SlackClient  # pragma: no cover


class SlackCLICommandHandler:
  """Slack CLI command handler.

  :param bot: The configured slack bot in use.
  """

  method_prefix = "command_"

  def __init__(self, slack_client: "SlackClient") -> None:
    self.slack_client = slack_client

  def handle(self, command_class: Type[SlackCommandBase]) -> None:
    """Handle a command class instance.

    :param command_class:  The command class to invoke.
    """
    instance = command_class(self.slack_client)
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
    """Post a realtime camera snapshot to Slack."""

    self.handle(commands.SnapshotCommand)

  def command_status(self) -> None:
    """Report the current status of the security system."""

    self.handle(commands.StatusCommand)

  def command_uptime(self) -> None:
    """Report the current uptime of this bot."""

    self.handle(commands.UptimeCommand)
