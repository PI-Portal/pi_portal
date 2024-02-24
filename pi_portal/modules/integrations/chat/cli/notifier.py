"""Notifier for the chat CLI."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.integrations.chat import TypeChatClient


class ChatCLINotifier:
  """Notifier for the chat CLI.

  :param client: The configured chat client to use.
  """

  def __init__(self, client: "TypeChatClient") -> None:
    self.chat_client = client

  def notify_already_start(self) -> None:
    """Report that the service is already up."""

    self.chat_client.send_message("Already running ...")

  def notify_already_stop(self) -> None:
    """Report that the service is already down."""

    self.chat_client.send_message("Already stopped ...")

  def notify_error(self) -> None:
    """Report that an error has occurred."""

    self.chat_client.send_message(
        "An internal error occurred ... you better take a look."
    )

  def notify_start(self) -> None:
    """Report that the service is starting."""

    self.chat_client.send_message("Starting ...")

  def notify_stop(self) -> None:
    """Report that the service is stopping."""

    self.chat_client.send_message("Shutting down ...")
