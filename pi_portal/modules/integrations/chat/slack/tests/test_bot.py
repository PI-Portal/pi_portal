"""Test the SlackBot class."""
from io import StringIO
from typing import cast
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.bases.bot import ChatBotBase
from pi_portal.modules.integrations.chat.slack import bot, config


@pytest.mark.usefixtures("test_state")
class TestSlackBot:
  """Test the SlackBot class."""

  def test_initialize__attributes(
      self,
      slack_bot_instance: bot.SlackBot,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]
    assert slack_bot_instance.channel_id == (
        slack_user_config['SLACK_CHANNEL_ID']
    )

  def test_initialize__configuration(
      self,
      slack_bot_instance: bot.SlackBot,
  ) -> None:
    assert isinstance(
        slack_bot_instance.configuration,
        config.SlackIntegrationConfiguration,
    )

  def test_initialize__slack_bolt_app(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_bolt_app: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]
    assert slack_bot_instance.app == mocked_slack_bolt_app.return_value
    mocked_slack_bolt_app.assert_called_once_with(
        signing_secret=slack_user_config['SLACK_APP_SIGNING_SECRET'],
        token=slack_user_config['SLACK_BOT_TOKEN'],
    )

  def test_initialize__slack_bolt_socket_handler(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_bolt_app: mock.Mock,
      mocked_slack_bolt_socket_handler: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]
    assert slack_bot_instance.web_socket == (
        mocked_slack_bolt_socket_handler.return_value
    )
    mocked_slack_bolt_socket_handler.assert_called_once_with(
        mocked_slack_bolt_app.return_value,
        slack_user_config['SLACK_APP_TOKEN'],
    )

  def test_initialize__slack_client(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_client: mock.Mock,
  ) -> None:
    assert slack_bot_instance.chat_client == mocked_slack_client.return_value
    mocked_slack_client.assert_called_once_with(propagate_exceptions=False)

  def test_initialize__inheritance(
      self,
      slack_bot_instance: bot.SlackBot,
  ) -> None:
    assert isinstance(
        slack_bot_instance,
        bot.SlackBot,
    )
    assert isinstance(
        slack_bot_instance,
        ChatBotBase,
    )

  def test_halt__logging(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_stream: StringIO,
  ) -> None:
    slack_bot_instance.halt()

    assert mocked_stream.getvalue() == \
        "WARNING - Chat Bot process has been terminated ...\n"

  def test_halt__bolt_app__calls_close(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_bolt_socket_handler: mock.Mock,
  ) -> None:
    slack_bot_instance.halt()

    mocked_slack_bolt_socket_handler.return_value.\
        close.assert_called_once_with()

  def test_halt__calls_os_exit(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_os_module: mock.Mock,
  ) -> None:
    slack_bot_instance.halt()

    # pylint: disable=protected-access
    mocked_os_module._exit.assert_called_once_with(1)

  def test_start__logging(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_stream: StringIO,
  ) -> None:
    slack_bot_instance.start()

    assert mocked_stream.getvalue() == \
        "WARNING - Chat Bot process has started.\n"

  def test_start__sends_chat_message(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_client: mock.Mock,
  ) -> None:
    slack_bot_instance.start()

    mocked_slack_client.return_value.send_message.assert_called_once_with(
        "I've rebooted!  Now listening for commands...",
    )

  def test_start__bolt_app__calls_start(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_bolt_socket_handler: mock.Mock,
  ) -> None:
    slack_bot_instance.start()

    mocked_slack_bolt_socket_handler.return_value.\
        start.assert_called_once_with()

  def test_start__bolt_app__creates_receiver(
      self,
      slack_bot_instance: bot.SlackBot,
      mocked_slack_bolt_app: mock.Mock,
  ) -> None:
    slack_bot_instance.start()

    mocked_slack_bolt_app.return_value.event.assert_called_once_with("message")

  def test_start__bolt_app__created_receiver__calls_handle_event(
      self,
      slack_bot_instance_mocked_handle_event: bot.SlackBot,
      mocked_handle_event_method: mock.Mock,
      mocked_slack_bolt_app: mock.Mock,
  ) -> None:
    test_event = cast(bot.TypeSlackBoltEvent, {})
    slack_bot_instance_mocked_handle_event.start()
    bolt_event_receiver = (
        mocked_slack_bolt_app.return_value.event.return_value.call_args[0][0]
    )

    bolt_event_receiver(test_event)

    mocked_handle_event_method.assert_called_once_with(test_event)

  @pytest.mark.parametrize("command", ["id", "help"])
  def test_handle_event__vary_command__valid_event__calls_handler(
      self,
      slack_bot_instance_mocked_handle_command: bot.SlackBot,
      mocked_handle_command_method: mock.Mock,
      command: str,
  ) -> None:
    test_event = bot.TypeSlackBoltEvent(
        channel=slack_bot_instance_mocked_handle_command.channel_id,
        text=command,
    )

    slack_bot_instance_mocked_handle_command.handle_event(test_event)

    mocked_handle_command_method.assert_called_once_with(command)

  @pytest.mark.parametrize("command", ["id", "help"])
  def test_handle_event__vary_command__no_channel__does_not_call_handler(
      self,
      slack_bot_instance_mocked_handle_command: bot.SlackBot,
      mocked_handle_command_method: mock.Mock,
      command: str,
  ) -> None:
    test_event = cast(bot.TypeSlackBoltEvent, {"text": command})

    slack_bot_instance_mocked_handle_command.handle_event(test_event)

    mocked_handle_command_method.assert_not_called()

  @pytest.mark.parametrize("command", ["id", "help"])
  def test_handle_event__vary_command__wrong_channel__does_not_call_handler(
      self,
      slack_bot_instance_mocked_handle_command: bot.SlackBot,
      mocked_handle_command_method: mock.Mock,
      command: str,
  ) -> None:
    test_event = bot.TypeSlackBoltEvent(
        channel="Invalid Channel",
        text=command,
    )

    slack_bot_instance_mocked_handle_command.handle_event(test_event)

    mocked_handle_command_method.assert_not_called()

  def test_handle_event__no_command__does_not_call_handler(
      self,
      slack_bot_instance_mocked_handle_command: bot.SlackBot,
      mocked_handle_command_method: mock.Mock,
  ) -> None:
    test_event = cast(bot.TypeSlackBoltEvent, {})

    slack_bot_instance_mocked_handle_command.handle_event(test_event)

    mocked_handle_command_method.assert_not_called()
