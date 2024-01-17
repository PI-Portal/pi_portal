"""Test the SlackBot class."""
from typing import cast
from unittest import mock

from pi_portal.modules.configuration import state
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations import slack
from pi_portal.modules.integrations.slack import bot, cli


class TestSlackBot:
  """Test the SlackBot class."""

  def test_initialize__attributes(
      self,
      bot_instance: bot.SlackBot,
  ) -> None:
    assert isinstance(bot_instance.app, mock.Mock)
    assert isinstance(bot_instance.log, mock.Mock)
    assert bot_instance.channel_id == mock_state.MOCK_SLACK_CHANNEL_ID
    assert bot_instance.command_list == cli.get_available_commands()
    assert isinstance(bot_instance.slack_client, mock.Mock)
    assert isinstance(bot_instance.web_socket, mock.Mock)

  def test_initialize__app(
      self,
      bot_instance: bot.SlackBot,
      mocked_state: state.State,
      mocked_slack_bolt_app: mock.Mock,
  ) -> None:
    slack_integration_config = mocked_state.user_config["CHAT"]["SLACK"]
    assert bot_instance.app == mocked_slack_bolt_app.return_value
    mocked_slack_bolt_app.assert_called_once_with(
        signing_secret=slack_integration_config["SLACK_APP_SIGNING_SECRET"],
        token=slack_integration_config['SLACK_BOT_TOKEN']
    )

  def test_initialize__client(
      self,
      bot_instance: bot.SlackBot,
      mocked_slack_client: mock.Mock,
  ) -> None:
    assert bot_instance.slack_client == mocked_slack_client.return_value

  def test_initialize__web_socket(
      self,
      bot_instance: bot.SlackBot,
      mocked_state: mock.Mock,
      mocked_slack_bolt_socket_handler: mock.Mock,
  ) -> None:
    slack_integration_config = mocked_state.user_config["CHAT"]["SLACK"]
    assert bot_instance.web_socket == \
        mocked_slack_bolt_socket_handler.return_value
    mocked_slack_bolt_socket_handler.assert_called_once_with(
        bot_instance.app,
        slack_integration_config['SLACK_APP_TOKEN'],
    )

  @mock.patch(slack.__name__ + ".cli.handler.SlackCLICommandHandler")
  def test_handle_command_valid(
      self,
      m_slack_cli: mock.Mock,
      bot_instance: bot.SlackBot,
      mocked_logger: mock.Mock,
  ) -> None:
    test_command = "id"
    m_slack_cli.return_value.method_prefix = "command_"

    bot_instance.handle_command(test_command)

    m_slack_cli.assert_called_once_with(bot=bot_instance)
    m_slack_cli.return_value.command_id.assert_called_once_with()
    mocked_logger.return_value.debug.assert_called_once_with(
        "Received command: '%s'", test_command
    )
    mocked_logger.return_value.info.assert_called_once_with(
        "Executing valid command: '%s'", test_command
    )

  @mock.patch(slack.__name__ + ".cli.handler.SlackCLICommandHandler")
  def test_handle_command_invalid(
      self,
      m_slack_cli: mock.Mock,
      bot_instance: bot.SlackBot,
      mocked_logger: mock.Mock,
  ) -> None:
    invalid_command = "Invalid Command"

    bot_instance.handle_command(invalid_command)

    m_slack_cli.return_value.command_id.assert_not_called()
    mocked_logger.return_value.debug.assert_called_once_with(
        "Received command: '%s'", invalid_command
    )

  def test_handle_event_valid(
      self,
      bot_instance: bot.SlackBot,
  ) -> None:
    with mock.patch.object(bot_instance, "handle_command") as m_handle:
      test_command = "id"
      test_event = bot.TypeSlackBoltEvent(
          channel=bot_instance.channel_id,
          text=test_command,
      )

      bot_instance.handle_event(test_event)

    m_handle.assert_called_once_with(test_command)

  def test_handle_event_no_channel(
      self,
      bot_instance: bot.SlackBot,
  ) -> None:
    with mock.patch.object(bot_instance, "handle_command") as m_handle:
      test_event = cast(bot.TypeSlackBoltEvent, {"text": "id"})

      bot_instance.handle_event(test_event)

    m_handle.assert_not_called()

  def test_handle_wrong_channel(
      self,
      bot_instance: bot.SlackBot,
  ) -> None:
    with mock.patch.object(bot_instance, "handle_command") as m_handle:
      test_command = "id"
      test_event = bot.TypeSlackBoltEvent(
          channel="Invalid Channel",
          text=test_command,
      )

      bot_instance.handle_event(test_event)

    m_handle.assert_not_called()

  def test_handle_no_command(
      self,
      bot_instance: bot.SlackBot,
  ) -> None:
    with mock.patch.object(bot_instance, "handle_command") as m_handle:

      test_event = cast(bot.TypeSlackBoltEvent, {})
      bot_instance.handle_event(test_event)

    m_handle.assert_not_called()

  def test_connect(
      self,
      bot_instance: bot.SlackBot,
      mocked_slack_client: mock.Mock,
      mocked_slack_bolt_app: mock.Mock,
      mocked_slack_bolt_socket_handler: mock.Mock,
  ) -> None:
    bot_instance.connect()

    mocked_slack_client.return_value.send_message.assert_called_once_with(
        "I've rebooted!  Now listening for commands...",
    )
    mocked_slack_bolt_app.return_value.event.assert_called_once_with("message")
    mocked_slack_bolt_socket_handler.return_value.start.assert_called_once_with(
    )
