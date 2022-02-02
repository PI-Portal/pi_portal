"""Slack CLI."""

from typing import TYPE_CHECKING, List, Type

from pi_portal.modules.integrations.slack_cli import commands
from pi_portal.modules.integrations.slack_cli.commands.bases import command

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import Client  # pragma: no cover


def get_available_commands() -> List[str]:
  """Retrieve a complete list of Slack CLI commands.

  :return: The complete list of Slack CLI commands.
  """
  command_list = []
  for method in dir(SlackCLI):
    if method.startswith(SlackCLI.method_prefix) is True:
      command_list.append(method.replace(SlackCLI.method_prefix, ''))
  return command_list


class SlackCLI:
  """The Slack Command Line Interface."""

  method_prefix = "command_"

  def __init__(self, client: "Client") -> None:
    self.slack_client = client

  def invoke(self, command_class: Type[command.CommandBase]) -> None:
    """Invoke a command class instance.

    :param command_class:  The command class to invoke.
    """
    instance = command_class(self.slack_client)
    instance.invoke()

  def command_id(self) -> None:
    """Report the logger ID the bot is currently running with."""

    self.invoke(commands.IDCommand)

  def command_arm(self) -> None:
    """Arm the security system."""

    self.invoke(commands.ArmCommand)

  def command_disarm(self) -> None:
    """Disarm the security system."""

    self.invoke(commands.DisarmCommand)

  def command_help(self) -> None:
    """Report the list of valid commands."""

    self.invoke(commands.HelpCommand)

  def command_restart(self) -> None:
    """Terminate the bot, and rely on supervisor to restart it."""

    self.invoke(commands.RestartCommand)

  def command_snapshot(self) -> None:
    """Post a realtime camera snapshot to Slack."""

    self.invoke(commands.SnapshotCommand)

  def command_status(self) -> None:
    """Report the current status of the security system."""

    self.invoke(commands.StatusCommand)

  def command_uptime(self) -> None:
    """Report the current uptime of this bot."""

    self.invoke(commands.UptimeCommand)
