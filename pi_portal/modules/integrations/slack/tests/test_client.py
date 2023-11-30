"""Test the SlackClient class."""

from typing import cast
from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations import motion
from pi_portal.modules.integrations.slack import client
from slack_sdk.errors import SlackRequestError


class TestSlackClient(TestCase):
  """Test the SlackClient class."""

  @mock_state.patch
  def setUp(self) -> None:
    self.slack_client = client.SlackClient()
    self.slack_client.motion_client = mock.MagicMock()
    self.slack_client.log = mock.Mock()

  def _mock_motion_client(self) -> mock.Mock:
    return cast(mock.Mock, self.slack_client.motion_client)

  def _mock_log(self) -> mock.Mock:
    return cast(mock.Mock, self.slack_client.log)

  @mock_state.patch
  def test_initialize(self) -> None:
    slack_client = client.SlackClient()
    self.assertEqual(slack_client.web.token, mock_state.MOCK_SLACK_BOT_TOKEN)
    self.assertIsInstance(slack_client.motion_client, motion.Motion)

  def test_send_message(self) -> None:
    test_message = "test message"
    self.slack_client.web = mock.MagicMock()

    self.slack_client.send_message(test_message)
    self.slack_client.web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel, text=test_message
    )

  def test_send_message_exception(self) -> None:
    test_message = "test message"
    with mock.patch.object(self.slack_client, "web") as m_web:
      m_web.chat_postMessage.side_effect = SlackRequestError("Boom!")
      self.slack_client.send_message(test_message)

    self.assertListEqual(
        m_web.chat_postMessage.mock_calls,
        [mock.call(
            channel=self.slack_client.channel,
            text=test_message,
        )] * self.slack_client.retries
    )
    self.assertListEqual(
        self._mock_log().error.mock_calls,
        [mock.call("Failed to send message: '%s'", test_message)] *
        self.slack_client.retries
    )

  def test_send_file(self) -> None:
    test_file = "/path/to/mock/file.txt"
    with mock.patch.object(self.slack_client, "web") as m_web:
      self.slack_client.send_file(test_file)

    m_web.files_upload.assert_called_once_with(
        channels=self.slack_client.channel,
        file=test_file,
        title=self.slack_client.config.upload_file_title
    )

  def test_send_file_exception(self) -> None:
    test_file = "/path/to/mock/file.txt"
    with mock.patch.object(self.slack_client, "web") as m_web:
      m_web.files_upload.side_effect = SlackRequestError("Boom!")
      self.slack_client.send_file(test_file)

    self.assertListEqual(
        m_web.files_upload.mock_calls, [
            mock.call(
                channels=self.slack_client.channel,
                file=test_file,
                title=self.slack_client.config.upload_file_title
            )
        ] * self.slack_client.retries
    )
    self.assertListEqual(
        self._mock_log().error.mock_calls,
        [mock.call("Failed to send file: '%s'", test_file)] *
        self.slack_client.retries
    )

  def test_send_snapshot(self) -> None:
    test_snapshot = "/path/to/mock/snapshot.jpg"
    with mock.patch.object(self.slack_client, "send_file") as m_send:
      self.slack_client.send_snapshot(test_snapshot)
    m_send.assert_called_once_with(test_snapshot)
    self._mock_motion_client().cleanup_snapshot.assert_called_once_with(
        test_snapshot,
    )

  def test_send_snapshot_exception(self) -> None:
    test_snapshot = "/path/to/mock/snapshot.jpg"
    with mock.patch.object(self.slack_client, "send_file") as m_send:
      with mock.patch.object(self.slack_client, "web") as m_web:
        self._mock_motion_client(
        ).cleanup_snapshot.side_effect = (motion.MotionException("Boom!"),)
        self.slack_client.send_snapshot(test_snapshot)

    m_send.assert_called_once_with(test_snapshot)
    self._mock_motion_client().cleanup_snapshot.assert_called_once_with(
        test_snapshot,
    )
    m_web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel,
        text="An error occurred cleaning up this snapshot.",
    )
    self._mock_log().error.assert_called_once_with(
        'Failed to remove old motion snapshot!',
    )

  def test_send_video(self) -> None:
    test_video = "/path/to/mock/video.mp4"
    with mock.patch.object(self.slack_client, "send_file") as m_send:
      self.slack_client.send_video(test_video)

    m_send.assert_called_once_with(test_video)
    self._mock_motion_client().archive_video.assert_called_once_with(test_video)

  def test_send_video_exception(self) -> None:
    test_video = "/path/to/mock/video.mp4"
    with mock.patch.object(self.slack_client, "send_file") as m_send:
      with mock.patch.object(self.slack_client, "web") as m_web:
        self._mock_motion_client(
        ).archive_video.side_effect = (motion.MotionException("Boom!"),)
        self.slack_client.send_video(test_video)

    m_send.assert_called_once_with(test_video)
    self._mock_motion_client().archive_video.assert_called_once_with(test_video)
    m_web.chat_postMessage.assert_called_once_with(
        channel=self.slack_client.channel,
        text="An error occurred archiving this video.",
    )
    self._mock_log().error.assert_called_once_with(
        "Failed to archive motion video capture!",
    )
