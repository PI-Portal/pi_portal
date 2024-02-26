"""Pi Portal Slack messaging client."""

from typing import Optional
from urllib.error import URLError

from pi_portal.modules.configuration.types.chat_config_type import (
    TypeUserConfigChatSlack,
)
from pi_portal.modules.integrations.chat.bases.client import (
    ChatClientBase,
    ChatClientError,
)
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError
from .config import SlackIntegrationConfiguration


class SlackClient(ChatClientBase[TypeUserConfigChatSlack]):
  """Slack messaging client."""

  configuration: SlackIntegrationConfiguration
  retries = 5

  def __init__(self, propagate_exceptions: bool) -> None:
    super().__init__(propagate_exceptions)
    self.configuration = SlackIntegrationConfiguration()
    self.configure_logger()
    self.channel = self.configuration.settings['SLACK_CHANNEL']
    self.channel_id = self.configuration.settings['SLACK_CHANNEL_ID']
    self.web_chat = WebClient(
        token=self.configuration.settings['SLACK_BOT_TOKEN'],
        timeout=30,
    )
    self.web_files = WebClient(
        token=self.configuration.settings['SLACK_BOT_TOKEN'],
        timeout=300,
    )

  def send_message(self, message: str) -> None:
    """Send a message with the Slack Web client.

    :param message: The message to send to Slack.
    :raises: :class:`ChatClientError`
    """
    raised_exception: Optional[Exception] = None

    for _ in range(0, self.retries):
      try:
        self.web_chat.chat_postMessage(channel=self.channel, text=message)
        break
      except (SlackClientError, URLError) as exc:
        self.log.warning(
            "Retrying failed message: '%s' !",
            message,
        )
        raised_exception = exc
    else:
      self.log.error("Failed to send message: '%s' !", message)
      if self.propagate_exceptions and raised_exception:
        raise ChatClientError from raised_exception

  def send_file(self, file_name: str, description: str) -> None:
    """Send a file with the Slack Web client.

    :param file_name: The path to upload to Slack.
    :param description: A description of the file being uploaded to Slack.
    :raises: :class:`ChatClientError`
    """
    raised_exception: Optional[Exception] = None

    for _ in range(0, self.retries):
      try:
        self.web_files.files_upload_v2(
            channel=self.channel_id,
            file=file_name,
            title=description,
        )
        break
      except (SlackClientError, URLError) as exc:
        self.log.warning(
            "Retrying failed file transmission: '%s' !",
            file_name,
        )
        raised_exception = exc
    else:
      self.log.error("Failed to send file: '%s' !", file_name)
      if self.propagate_exceptions and raised_exception:
        raise ChatClientError from raised_exception
