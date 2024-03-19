"""Slack implementation of a chatbot."""

import os
from typing import Callable, cast

from pi_portal.modules.collections.limited_dictionary import LimitedDictionary
from pi_portal.modules.configuration.types.chat_config_type import (
    TypeUserConfigChatSlack,
)
from pi_portal.modules.integrations.chat.bases.bot import ChatBotBase
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from typing_extensions import NotRequired, TypedDict
from .config import SlackIntegrationConfiguration


class TypeSlackBoltEvent(TypedDict):
  """Typed representation of a Slack Bolt message event."""

  channel: str
  client_msg_id: NotRequired[str]
  text: str


class SlackBot(ChatBotBase[TypeUserConfigChatSlack]):
  """Slack implementation of a chatbot."""

  configuration: SlackIntegrationConfiguration

  def __init__(self) -> None:
    super().__init__()
    self.configuration = SlackIntegrationConfiguration()
    self.app = App(
        signing_secret=self.configuration.settings['SLACK_APP_SIGNING_SECRET'],
        token=self.configuration.settings['SLACK_BOT_TOKEN'],
    )
    self.channel_id = self.configuration.settings['SLACK_CHANNEL_ID']
    self.filter: LimitedDictionary[str, bool] = LimitedDictionary(10)
    self.web_socket = SocketModeHandler(
        self.app,
        self.configuration.settings['SLACK_APP_TOKEN'],
    )

  def halt(self) -> None:
    """Stop the chatbot."""

    self.log.warning("Chat Bot process has been terminated ...")

    # BaseSocketModeHandler is untyped
    close = cast(Callable[[], None], self.web_socket.close)
    close()
    os._exit(1)  # pylint: disable=protected-access

  def start(self) -> None:
    """Start the chatbot."""

    @self.app.event("message")
    def receiver(event: TypeSlackBoltEvent) -> None:
      """Receive messages from the Bolt Slack Bot subscription.

      :param event: An unvalidated Slack Bot message event.
      """
      self.log.debug("Slack Bolt event.", extra={"event": event})

      if not self._is_duplicate_event(event):
        self.handle_event(event)

    self.task_scheduler_client.chat_send_message(
        "I've rebooted!  Now listening for commands..."
    )
    self.log.warning("Chat Bot process has started.")

    # BaseSocketModeHandler is untyped
    start = cast(Callable[[], None], self.web_socket.start)
    start()

  def _is_duplicate_event(self, event: TypeSlackBoltEvent) -> bool:
    unique_id = event.get("client_msg_id", None)
    if unique_id:
      if unique_id in self.filter:
        return True
      self.filter[unique_id] = True
    return False

  def handle_event(self, event: TypeSlackBoltEvent) -> None:
    """Validate a bot message bound for this Slack Bot's channel.

    :param event: An unvalidated Slack Bot message event.
    """

    if self._is_valid_channel(event) and event["text"]:
      command = event["text"].lower()
      self.handle_command(command)

  def _is_valid_channel(self, event: TypeSlackBoltEvent) -> bool:
    if 'channel' not in event:
      return False
    if event['channel'] != self.channel_id:
      return False
    return True
