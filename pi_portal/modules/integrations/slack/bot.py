"""Pi Portal Slack RTM bot."""

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.slack import cli, client
from pi_portal.modules.integrations.slack.cli import handler
from pi_portal.modules.mixins import log_file
from slack_sdk.rtm_v2 import RTMClient
from typing_extensions import TypedDict


class TypeEvent(TypedDict):
  """Typed representation of a Slack RTM event."""

  channel: str
  text: str


class SlackBot(log_file.WriteLogFile):
  """Slack RTM bot."""

  logger_name = "bot"
  log_file_path = config.SLACK_BOT_LOGFILE_PATH

  def __init__(self) -> None:
    current_state = state.State()
    self.configure_logger()
    self.rtm = RTMClient(token=current_state.user_config["SLACK_BOT_TOKEN"])
    self.channel_id = current_state.user_config['SLACK_CHANNEL_ID']
    self.command_list = cli.get_available_commands()
    self.slack_client = client.SlackClient()

  def connect(self) -> None:
    """Connect to Slack via a RTM subscription."""

    @self.rtm.on("message")
    def receiver(_: RTMClient, event: TypeEvent) -> None:
      """Receive messages on the RTM subscription.

      :param event: An unvalidated Slack RTM event message.
      """

      self.handle_event(event)  # pragma: no cover

    self.slack_client.send_message(
        "I've rebooted!  Now listening for commands..."
    )
    self.log.warning("Slack Bot process has started.")
    self.rtm.start()

  def handle_event(self, event: TypeEvent) -> None:
    """Validate a RTM message bound for this bot's channel.

    :param event: An unvalidated Slack RTM event message.
    """

    if self._is_valid_channel(event) and 'text' in event:
      command = event['text'].lower()
      self.handle_command(command)

  def _is_valid_channel(self, event: TypeEvent) -> bool:
    if 'channel' not in event:
      return False
    if event['channel'] != self.channel_id:
      return False
    return True

  def handle_command(self, command: str) -> None:
    """Handle a CLI command by name.

    :param command: The Slack CLI command to handle.
    """

    self.log.debug("Received command: '%s'", command)
    if command in self.command_list:
      self.log.info("Executing valid command: '%s'", command)
      command_handler = handler.SlackCLICommandHandler(bot=self)
      getattr(command_handler, command_handler.method_prefix + command)()
