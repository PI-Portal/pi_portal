"""Pi Portal Slack Bolt bot."""

from typing import Callable, cast

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.slack import cli, client
from pi_portal.modules.integrations.slack.cli import handler
from pi_portal.modules.mixins import write_log_file
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from typing_extensions import TypedDict


class TypeSlackBoltEvent(TypedDict):
  """Typed representation of a Slack Bolt message event."""

  channel: str
  text: str


class SlackBot(write_log_file.LogFileWriter):
  """Slack bot."""

  logger_name = "bot"
  log_file_path = config.SLACK_BOT_LOGFILE_PATH
  web_socket: SocketModeHandler

  def __init__(self) -> None:
    current_state = state.State()
    self.app = App(
        signing_secret=current_state.user_config['SLACK_APP_SIGNING_SECRET'],
        token=current_state.user_config['SLACK_BOT_TOKEN'],
    )
    self.configure_logger()
    self.channel_id = current_state.user_config['SLACK_CHANNEL_ID']
    self.command_list = cli.get_available_commands()
    self.slack_client = client.SlackClient()
    self.web_socket = SocketModeHandler(
        self.app,
        current_state.user_config['SLACK_APP_TOKEN'],
    )

  def connect(self) -> None:
    """Start the Slack bot."""

    @self.app.event("message")
    def receiver(event: TypeSlackBoltEvent) -> None:
      """Receive messages from the Bolt Slack Bot subscription.

      :param event: An unvalidated Slack Bot message event.
      """

      self.handle_event(event)  # pragma: no cover

    self.slack_client.send_message(
        "I've rebooted!  Now listening for commands..."
    )
    self.log.warning("Slack Bot process has started.")

    # BaseSocketModeHandler is untyped
    start = cast(Callable[[], None], self.web_socket.start)
    start()

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

  def handle_command(self, command: str) -> None:
    """Handle a CLI command by name.

    :param command: The Slack CLI command to handle.
    """

    self.log.debug("Received command: '%s'", command)
    if command in self.command_list:
      self.log.info("Executing valid command: '%s'", command)
      command_handler = handler.SlackCLICommandHandler(bot=self)
      getattr(command_handler, command_handler.method_prefix + command)()
