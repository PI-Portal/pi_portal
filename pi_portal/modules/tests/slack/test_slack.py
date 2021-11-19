"""Test Slack client configuration."""

from unittest import TestCase, mock

from pi_portal.modules import motion, slack
from pi_portal.modules.tests.fixtures import mock_state
from slack_sdk.errors import SlackRequestError


class TestSlackClient(TestCase):
  """Test the ClientConfiguration class."""

  @mock_state.patch
  def setUp(self):
    self.slack_client = slack.Client()
    self.slack_client.motion_client = mock.MagicMock()

  @mock_state.patch
  def test_initialize(self):
    client = slack.Client()
    self.assertEqual(client.web.token, mock_state.MOCK_SLACK_TOKEN)
    self.assertEqual(client.rtm.token, mock_state.MOCK_SLACK_TOKEN)
    self.assertEqual(client.channel, mock_state.MOCK_SLACK_CHANNEL)
    self.assertEqual(client.channel_id, mock_state.MOCK_SLACK_CHANNEL_ID)
    self.assertIsInstance(client.motion_client, motion.Motion)
    self.assertIsInstance(client.config, slack.ClientConfiguration)

  @mock.patch(slack.__name__ + ".slack_cli.SlackCLI")
  def test_handle_event_invalid_command(self, m_slack_cli):
    m_slack_cli.return_value.prefix = "command_"
    m_slack_cli.return_value.get_commands.return_value = ['command_id']
    test_event = {
        "text": "invalid_command"
    }
    self.slack_client.handle_event(test_event)
    m_slack_cli.return_value.command_id.assert_not_called()

  @mock.patch(slack.__name__ + ".slack_cli.SlackCLI")
  def test_handle_event_valid_command(self, m_slack_cli):
    m_slack_cli.return_value.prefix = "command_"
    m_slack_cli.return_value.get_commands.return_value = ['command_id']
    test_event = {
        "text": "id"
    }
    self.slack_client.handle_event(test_event)
    m_slack_cli.return_value.command_id.assert_called_once_with()

  def test_handle_rtm_message_no_channel(self):
    self.slack_client.handle_event = mock.MagicMock()
    test_event = {}
    self.slack_client.handle_rtm_message(test_event)
    self.slack_client.handle_event.assert_not_called()

  def test_handle_rtm_message_no_text(self):
    self.slack_client.handle_event = mock.MagicMock()
    test_event = {
        'channel': 'mockChannel'
    }
    self.slack_client.handle_rtm_message(test_event)
    self.slack_client.handle_event.assert_not_called()

  def test_handle_rtm_message_wrong_channel(self):
    self.slack_client.handle_event = mock.MagicMock()
    test_event = {
        'channel': 'mockChannel',
        'text': "hello"
    }
    self.slack_client.handle_rtm_message(test_event)
    self.slack_client.handle_event.assert_not_called()

  def test_handle_rtm_message_valid_event(self):
    self.slack_client.handle_event = mock.MagicMock()
    test_event = {
        'channel': self.slack_client.channel_id,
        'text': "hello"
    }
    self.slack_client.handle_rtm_message(test_event)
    self.slack_client.handle_event.assert_called_once_with(test_event)

  def test_send_message(self):
    test_message = "test message"
    self.slack_client.web = mock.MagicMock()
    self.slack_client.send_message(test_message)
    self.slack_client.web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel, text=test_message
    )

  def test_test_send_message_exception(self):
    test_message = "test message"
    self.slack_client.web = mock.MagicMock()
    self.slack_client.web.chat_postMessage.side_effect = (
        SlackRequestError("Boom!")
    )
    self.slack_client.send_message(test_message)
    self.assertListEqual(
        self.slack_client.web.chat_postMessage.mock_calls,
        [mock.call(
            channel=self.slack_client.channel,
            text=test_message,
        )] * self.slack_client.retries
    )

  def test_send_file(self):
    test_file = "/path/to/mock/file.txt"
    self.slack_client.web = mock.MagicMock()
    self.slack_client.send_file(test_file)
    self.slack_client.web.files_upload.assert_called_once_with(
        channels=self.slack_client.channel,
        file=test_file,
        title=self.slack_client.config.upload_file_title
    )

  def test_send_file_exception(self):
    test_file = "/path/to/mock/file.txt"
    self.slack_client.web = mock.MagicMock()
    self.slack_client.web.files_upload.side_effect = (
        SlackRequestError("Boom!")
    )
    self.slack_client.send_file(test_file)
    self.assertListEqual(
        self.slack_client.web.files_upload.mock_calls, [
            mock.call(
                channels=self.slack_client.channel,
                file=test_file,
                title=self.slack_client.config.upload_file_title
            )
        ] * self.slack_client.retries
    )

  def test_send_video(self):
    test_video = "/path/to/mock/video.mp4"
    self.slack_client.send_file = mock.MagicMock()
    self.slack_client.send_video(test_video)
    self.slack_client.send_file.assert_called_once_with(test_video)
    self.slack_client.motion_client.archive_video_to_s3.assert_called_once_with(
        test_video
    )

  def test_send_video_exception(self):
    test_video = "/path/to/mock/video.mp4"
    self.slack_client.web = mock.MagicMock()
    self.slack_client.motion_client.archive_video_to_s3.side_effect = (
        motion.MotionException("Boom!")
    )
    self.slack_client.send_file = mock.MagicMock()
    self.slack_client.send_video(test_video)
    self.slack_client.send_file.assert_called_once_with(test_video)
    self.slack_client.motion_client.archive_video_to_s3.assert_called_once_with(
        test_video
    )
    self.slack_client.web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel,
        text="An error occurred archiving this video.",
    )

  def test_subscribe(self):
    self.slack_client.rtm = mock.MagicMock()
    self.slack_client.web = mock.MagicMock()

    self.slack_client.subscribe()
    self.slack_client.web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel,
        text="I've rebooted!  Now listening for commands...",
    )
    self.slack_client.rtm.on.assert_called_once_with("message")
    self.slack_client.rtm.start.assert_called_once_with()
