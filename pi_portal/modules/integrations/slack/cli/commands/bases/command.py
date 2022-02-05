"""Base command class for Slack CLI commands."""

import abc
from typing import TYPE_CHECKING

from pi_portal.modules.integrations.slack.cli.notifier import SlackCLINotifier

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.bot import \
      SlackBot  # pragma: no cover


class SlackCommandBase(abc.ABC):
  """A base command for the Slack CLI.

  :param bot: The configured slack bot in use.
  """

  def __init__(self, bot: "SlackBot") -> None:
    self.notifier = SlackCLINotifier(bot.slack_client)
    self.slack_bot = bot

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke the this command."""
