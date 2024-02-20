"""Chat CLI."""

from typing import List

from pi_portal.modules.integrations.slack.cli import commands, handler
from pi_portal.modules.integrations.slack.cli.commands.bases.command import (
    ChatCommandBase,
)


def get_available_commands() -> List[str]:
  """Retrieve a complete list of chat CLI commands.

  :returns: The complete list of chat CLI commands.
  """
  command_list = []
  for method in dir(handler.ChatCLICommandHandler):
    if method.startswith(handler.ChatCLICommandHandler.method_prefix) is True:
      command_list.append(
          method.replace(handler.ChatCLICommandHandler.method_prefix, '')
      )
  return command_list
