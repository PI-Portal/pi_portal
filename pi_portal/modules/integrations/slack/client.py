"""Pi Portal Slack messaging client."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.motion import client as motion_client
from pi_portal.modules.integrations.slack import config as slack_config
from pi_portal.modules.mixins import write_archived_log_file
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError, SlackRequestError


class SlackClient(write_archived_log_file.ArchivedLogFileWriter):
  """Slack messaging client."""

  logger_name = "client"
  log_file_path = config.LOG_FILE_CHAT_CLIENT
  retries = 5

  def __init__(self) -> None:
    current_state = state.State()
    slack_integration_config = current_state.user_config["CHAT"]["SLACK"]
    self.configure_logger()
    self.web = WebClient(token=slack_integration_config['SLACK_BOT_TOKEN'])
    self.channel = slack_integration_config['SLACK_CHANNEL']
    self.channel_id = slack_integration_config['SLACK_CHANNEL_ID']
    self.motion_client = motion_client.MotionClient(self.log)
    self.config = slack_config.SlackClientConfiguration()

  def send_message(self, message: str) -> None:
    """Send a message with the Slack Web client.

    :param message: The message to send to Slack.
    """

    for _ in range(0, self.retries):
      try:
        self.web.chat_postMessage(channel=self.channel, text=message)
        break
      except (SlackRequestError, SlackApiError):
        self.log.error("Failed to send message: '%s'", message)

  def send_file(self, file_name: str, description: str) -> None:
    """Send a file with the Slack Web client.

    :param file_name: The path to upload to Slack.
    :param description: A description of the file being uploaded to Slack.
    """

    for _ in range(0, self.retries):
      try:
        self.web.files_upload_v2(
            channel=self.channel_id,
            file=file_name,
            title=description,
        )
        break
      except (SlackRequestError, SlackApiError):
        self.log.error("Failed to send file: '%s'", file_name)
