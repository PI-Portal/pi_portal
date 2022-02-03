"""Slack CLI."""

from typing import List

from pi_portal.modules.integrations.slack.cli import commands, handler
from pi_portal.modules.integrations.slack.cli.commands.bases.command import (
    SlackCommandBase,
)


def get_available_commands() -> List[str]:
  """Retrieve a complete list of Slack CLI commands.

  :returns: The complete list of Slack CLI commands.
  """
  command_list = []
  for method in dir(handler.SlackCLICommandHandler):
    if method.startswith(handler.SlackCLICommandHandler.method_prefix) is True:
      command_list.append(
          method.replace(handler.SlackCLICommandHandler.method_prefix, '')
      )
  return command_list
