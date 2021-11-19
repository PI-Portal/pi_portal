"""Slack Integration."""

from pi_portal.modules import motion, slack_cli, state
from pi_portal.modules.logger import LOG_UUID
from slack_sdk import WebClient
from slack_sdk.rtm_v2 import RTMClient


class ClientConfiguration:
  """Configuration for the Slack integration."""

  log_uuid = LOG_UUID
  interval = 1
  upload_file_title = "Motion Upload"


class Client:
  """Client for integrating with Slack."""

  retries = 5

  def __init__(self):
    current_state = state.State()
    self.web = WebClient(token=current_state.user_config['SLACK_BOT_TOKEN'])
    self.rtm = RTMClient(token=current_state.user_config["SLACK_BOT_TOKEN"])
    self.channel = current_state.user_config['SLACK_CHANNEL']
    self.channel_id = current_state.user_config['SLACK_CHANNEL_ID']
    self.motion_client = motion.Motion()
    self.config = ClientConfiguration()

  def handle_event(self, event: dict):
    """Process a validated event, and call any valid commands.

    :param event: A validated Slack RTM event message.
    """

    cli = slack_cli.SlackCLI(client=self)
    command = cli.prefix + event['text'].lower()
    command_list = cli.get_commands()
    if command in command_list:
      getattr(cli, command)()

  def handle_rtm_message(self, event: dict):
    """Validate a RTM message bound for this bot's channel.

    :param event: An unvalidated Slack RTM event message.
    """

    if 'channel' not in event or 'text' not in event:
      return
    if event['channel'] != self.channel_id:
      return
    self.handle_event(event)

  def send_message(self, message: str):
    """Send a message with the Slack Web client.

    :param message: The message to send to Slack.
    """

    self.web.chat_postMessage(channel=self.channel, text=message)

  def send_file(self, file_name: str):
    """Send a file with the Slack Web client.

    :param file_name: The path to upload to Slack.
    """

    for _ in range(0, self.retries):
      try:
        response = self.web.files_upload(
            channels=self.channel,
            file=file_name,
            title=self.config.upload_file_title,
        )
        return response
      finally:
        pass

  def send_video(self, file_name: str):
    """Send a video to Slack, and have motion archive it in S3.

    :param file_name: The path of the file to process.
    """

    try:
      self.send_file(file_name)
      self.motion_client.archive_video_to_s3(file_name)
    except motion.MotionException:
      self.send_message("An error occurred archiving this video.")

  def subscribe(self):
    """Create a RTM subscription."""

    @self.rtm.on("message")
    def handler(_, event: dict):
      """Intercept messages on the RTM subscription.

      :param event: An unvalidated Slack RTM event message.
      """

      self.handle_rtm_message(event)  # pragma: no cover

    self.rtm.start()
