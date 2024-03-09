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
  message_retries = 3

  def __init__(self) -> None:
    super().__init__()
    self.configuration = SlackIntegrationConfiguration()
    self.configure_logger()
    self.channel = self.configuration.settings['SLACK_CHANNEL']
    self.channel_id = self.configuration.settings['SLACK_CHANNEL_ID']
    self.web_client_messages = WebClient(
        token=self.configuration.settings['SLACK_BOT_TOKEN'],
        timeout=30,
    )
    self.web_client_files = WebClient(
        token=self.configuration.settings['SLACK_BOT_TOKEN'],
        timeout=self.configuration.settings['SLACK_FILE_TRANSFER_TIMEOUT'],
    )

  def send_message(self, message: str) -> None:
    """Send a message with the Slack Web client.

    :param message: The message to send to Slack.
    :raises: :class:`ChatClientError`
    """
    raised_exception: Optional[Exception] = None

    for _ in range(0, self.message_retries):
      try:
        self.web_client_messages.chat_postMessage(
            channel=self.channel,
            text=message,
        )
        break
      except (SlackClientError, URLError) as exc:
        self.log.warning(
            "Retrying failed message: '%s' !",
            message,
        )
        raised_exception = exc
    else:
      self.log.error("Failed to send message: '%s' !", message)
      raise ChatClientError from raised_exception

  def send_file(self, file_name: str, description: str) -> None:
    """Send a file with the Slack Web client.

    :param file_name: The path to upload to Slack.
    :param description: A description of the file being uploaded to Slack.
    :raises: :class:`ChatClientError`
    """
    try:
      self.log.debug("Starting file transfer: '%s' ...", file_name)
      self.web_client_files.files_upload_v2(
          channel=self.channel_id,
          file=file_name,
          title=description,
      )
      self.log.debug("File transfer: '%s' complete !", file_name)
    except (SlackClientError, URLError) as exc:
      self.log.error("Failed to transfer file: '%s' !", file_name)
      raise ChatClientError from exc
