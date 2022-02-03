"""Base command class for Slack CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.modules.integrations.slack.cli.notifier import SlackCLINotifier

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.client import \
      SlackClient  # pragma: no cover


class SlackCommandBase(abc.ABC):
  """A base command for the Slack CLI.

  :param client: The configured slack client to use.
  """

  def __init__(self, client: "SlackClient") -> None:
    self.notifier = SlackCLINotifier(client)
    self.slack_client = client

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke the this command."""
