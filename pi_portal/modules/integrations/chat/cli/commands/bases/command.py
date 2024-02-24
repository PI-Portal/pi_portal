"""Base command class for chat CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.cli_commands.bases import command
from pi_portal.modules.integrations.chat.cli.notifier import ChatCLINotifier

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.integrations.chat import TypeChatBot


class ChatCommandBase(command.CommandBase, abc.ABC):
  """A base command for the chat CLI.

  :param bot: The configured chatbot in use.
  """

  def __init__(self, bot: "TypeChatBot") -> None:
    self.notifier = ChatCLINotifier(bot.chat_client)
    self.chatbot = bot
