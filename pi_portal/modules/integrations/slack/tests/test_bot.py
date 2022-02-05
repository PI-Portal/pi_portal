"""Test the SlackBot class."""

from typing import cast
from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations import slack
from pi_portal.modules.integrations.slack import bot, cli, client


class TestSlackBot(TestCase):
  """Test the SlackBot class."""

  @mock_state.patch
  def setUp(self) -> None:
    self.test_command = 'id'
    self.command_list = ['id']
    self.bot = bot.SlackBot()
    self.bot.slack_client = mock.MagicMock()
    self.bot.command_list = self.command_list

  @mock_state.patch
  def test_initialize(self) -> None:
    slack_bot = bot.SlackBot()
    self.assertEqual(slack_bot.rtm.token, mock_state.MOCK_SLACK_TOKEN)
    self.assertEqual(slack_bot.channel_id, mock_state.MOCK_SLACK_CHANNEL_ID)
    self.assertListEqual(slack_bot.command_list, cli.get_available_commands())
    self.assertIsInstance(slack_bot.slack_client, client.SlackClient)

  @mock.patch(slack.__name__ + ".cli.handler.SlackCLICommandHandler")
  def test_handle_command_valid(self, m_slack_cli: mock.Mock) -> None:
    m_slack_cli.return_value.method_prefix = "command_"

    self.bot.handle_command(self.test_command)
    m_slack_cli.assert_called_once_with(bot=self.bot)
    m_slack_cli.return_value.command_id.assert_called_once_with()

  @mock.patch(slack.__name__ + ".cli.handler.SlackCLICommandHandler")
  def test_handle_command_invalid(self, m_slack_cli: mock.Mock) -> None:
    invalid_command = "Invalid Command"
    self.bot.handle_command(invalid_command)
    m_slack_cli.return_value.command_id.assert_not_called()

  def test_handle_event_valid(self) -> None:
    test_event = bot.TypeEvent(
        channel=self.bot.channel_id, text=self.test_command
    )

    with mock.patch.object(self.bot, "handle_command") as m_handle:
      self.bot.handle_event(test_event)

    m_handle.assert_called_once_with(self.test_command)

  def test_handle_event_no_channel(self) -> None:
    test_event = cast(bot.TypeEvent, {"text": "id"})

    with mock.patch.object(self.bot, "handle_command") as m_handle:
      self.bot.handle_event(test_event)

    m_handle.assert_not_called()

  def test_handle_wrong_channel(self) -> None:
    test_event = bot.TypeEvent(
        channel="Invalid Channel", text=self.test_command
    )

    with mock.patch.object(self.bot, "handle_command") as m_handle:
      self.bot.handle_event(test_event)

    m_handle.assert_not_called()

  def test_handle_no_command(self) -> None:
    test_event = cast(bot.TypeEvent, {})

    with mock.patch.object(self.bot, "handle_command") as m_handle:
      self.bot.handle_event(test_event)

    m_handle.assert_not_called()

  def test_connect(self) -> None:
    with mock.patch.object(self.bot, "rtm") as m_rtm:
      with mock.patch.object(self.bot, "slack_client") as m_client:
        self.bot.connect()

    m_client.send_message.assert_called_once_with(
        "I've rebooted!  Now listening for commands...",
    )
    m_rtm.on.assert_called_once_with("message")
    m_rtm.start.assert_called_once_with()
