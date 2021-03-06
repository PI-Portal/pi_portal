"""Pi Portal Slack messaging client."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations import motion
from pi_portal.modules.integrations.slack import config as slack_config
from pi_portal.modules.mixins import log_file
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError, SlackRequestError


class SlackClient(log_file.WriteLogFile):
  """Slack messaging client."""

  logger_name = "client"
  log_file_path = config.SLACK_CLIENT_LOGFILE_PATH
  retries = 5

  def __init__(self) -> None:
    current_state = state.State()
    self.configure_logger()
    self.web = WebClient(token=current_state.user_config['SLACK_BOT_TOKEN'])
    self.channel = current_state.user_config['SLACK_CHANNEL']
    self.motion_client = motion.Motion()
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

  def send_file(self, file_name: str) -> None:
    """Send a file with the Slack Web client.

    :param file_name: The path to upload to Slack.
    """

    for _ in range(0, self.retries):
      try:
        self.web.files_upload(
            channels=self.channel,
            file=file_name,
            title=self.config.upload_file_title,
        )
        break
      except (SlackRequestError, SlackApiError):
        self.log.error("Failed to send file: '%s'", file_name)

  def send_snapshot(self, file_name: str) -> None:
    """Send a snapshot to Slack, and erase it locally.

    :param file_name: The path of the file to process.
    """

    try:
      self.send_file(file_name)
      self.motion_client.cleanup_snapshot(file_name)
    except motion.MotionException:
      self.send_message("An error occurred cleaning up this snapshot.")
      self.log.error("Failed to remove old motion snapshot!")

  def send_video(self, file_name: str) -> None:
    """Send a video to Slack, and have motion archive it in S3.

    :param file_name: The path of the file to process.
    """

    try:
      self.send_file(file_name)
      self.motion_client.archive_video(file_name)
    except motion.MotionException:
      self.send_message("An error occurred archiving this video.")
      self.log.error("Failed to archive motion video capture!")
