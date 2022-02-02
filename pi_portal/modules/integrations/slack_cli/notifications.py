"""Notifier for the Slack CLI."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import Client  # pragma: no cover


class SlackNotifier:
  """Notifier for the Slack CLI."""

  def __init__(self, client: "Client") -> None:
    self.slack_client = client

  def notify_already_start(self) -> None:
    """Report that the service is already up."""

    self.slack_client.send_message("Already running ...")

  def notify_already_stop(self) -> None:
    """Report that the service is already down."""

    self.slack_client.send_message("Already stopped ...")

  def notify_error(self) -> None:
    """Report that an error has occurred."""

    self.slack_client.send_message(
        "An internal error occurred ... you better take a look."
    )

  def notify_start(self) -> None:
    """Report that the service is starting."""

    self.slack_client.send_message("Starting ...")

  def notify_stop(self) -> None:
    """Report that the service is stopping."""

    self.slack_client.send_message("Shutting down ...")
