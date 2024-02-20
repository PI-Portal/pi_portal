"""Base command class for chat CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.cli_commands.bases import command
from pi_portal.modules.integrations.slack.cli.notifier import ChatCLINotifier

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.bot import \
      SlackBot  # pragma: no cover


class ChatCommandBase(command.CommandBase, abc.ABC):
  """A base command for the chat CLI.

  :param bot: The configured chatbot in use.
  """

  def __init__(self, bot: "SlackBot") -> None:
    self.notifier = ChatCLINotifier(bot.chat_client)
    self.chatbot = bot
