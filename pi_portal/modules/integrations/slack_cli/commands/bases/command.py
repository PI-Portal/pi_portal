"""Base command class for Slack CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.modules.integrations.slack_cli.notifications import SlackNotifier

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import Client  # pragma: no cover


class CommandBase(abc.ABC):
  """A base command for the Slack CLI.

  :param client: The configured slack client to use.
  """

  def __init__(self, client: "Client") -> None:
    self.notifier = SlackNotifier(client)
    self.slack_client = client

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke the this command."""
