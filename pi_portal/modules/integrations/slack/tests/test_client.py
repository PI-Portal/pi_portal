"""Test the SlackClient class."""

from unittest import mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.motion import client as motion_client
from pi_portal.modules.integrations.slack import client as slack_client
from pi_portal.modules.integrations.slack import config as slack_config
from slack_sdk.errors import SlackRequestError


class TestSlackClient:
  """Test the SlackClient class."""

  def test_initialize__attributes(
      self,
      client_instance: slack_client.SlackClient,
  ) -> None:
    assert isinstance(client_instance.web, mock.Mock)
    assert client_instance.channel == mock_state.MOCK_SLACK_CHANNEL
    assert client_instance.channel_id == mock_state.MOCK_SLACK_CHANNEL_ID
    assert isinstance(client_instance.motion_client, mock.Mock)
    assert isinstance(
        client_instance.config,
        slack_config.SlackClientConfiguration,
    )

  def test_initialize__web(
      self,
      client_instance: slack_client.SlackClient,
      mocked_state: mock.Mock,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    assert client_instance.web == mocked_slack_web_client.return_value
    mocked_slack_web_client.assert_called_once_with(
        token=mocked_state.user_config['SLACK_BOT_TOKEN']
    )

  def test_initialize__motion(
      self,
      client_instance: slack_client.SlackClient,
      mocked_motion_client: mock.Mock,
  ) -> None:
    assert client_instance.motion_client == mocked_motion_client.return_value
    mocked_motion_client.assert_called_once_with()

  def test_send_message__success(
      self,
      client_instance: slack_client.SlackClient,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_message = "test message"

    client_instance.send_message(test_message)

    mocked_slack_web_client.return_value.chat_postMessage.\
        assert_called_once_with(
          channel=client_instance.channel,
          text=test_message,
        )

  def test_send_message__exception(
      self,
      client_instance: slack_client.SlackClient,
      mocked_logger: mock.Mock,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client.return_value.chat_postMessage.side_effect = \
        SlackRequestError("Boom!")

    client_instance.send_message(test_message)

    assert mocked_slack_web_client.return_value.chat_postMessage.\
        mock_calls == \
        [
             mock.call(
               channel=client_instance.channel,
               text=test_message,
             ),
        ] * client_instance.retries
    assert mocked_logger.mock_calls == \
        [mock.call()] + \
        [
            mock.call().error("Failed to send message: '%s'", test_message),
        ] * client_instance.retries

  def test_send_file__success(
      self,
      client_instance: slack_client.SlackClient,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_file = "/path/to/mock/file.txt"

    client_instance.send_file(test_file)

    mocked_slack_web_client.return_value.files_upload_v2.\
        assert_called_once_with(
            channel=client_instance.channel_id,
            file=test_file,
            title=client_instance.config.upload_file_title
        )

  def test_send_file__exception(
      self,
      client_instance: slack_client.SlackClient,
      mocked_logger: mock.Mock,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_file = "/path/to/mock/file.txt"
    mocked_slack_web_client.return_value.files_upload_v2.side_effect = \
        SlackRequestError("Boom!")

    client_instance.send_file(test_file)

    assert mocked_slack_web_client.return_value.files_upload_v2.\
        mock_calls == \
        [
             mock.call(
               channel=client_instance.channel_id,
               file=test_file,
               title=client_instance.config.upload_file_title
             )
        ] * client_instance.retries
    assert mocked_logger.mock_calls == \
        [mock.call()] + \
        [
            mock.call().error("Failed to send file: '%s'", test_file),
        ] * client_instance.retries

  def test_send_snapshot__success(
      self,
      client_instance: slack_client.SlackClient,
      mocked_motion_client: mock.Mock,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_snapshot = "/path/to/mock/snapshot.jpg"

    client_instance.send_snapshot(test_snapshot)

    mocked_slack_web_client.return_value.files_upload_v2.\
        assert_called_once_with(
          channel=client_instance.channel_id,
          file=test_snapshot,
          title=client_instance.config.upload_file_title
        )
    mocked_motion_client.return_value.cleanup_snapshot.\
        assert_called_once_with(
          test_snapshot
        )

  def test_send_snapshot__exception(
      self,
      client_instance: slack_client.SlackClient,
      mocked_logger: mock.Mock,
      mocked_motion_client: mock.Mock,
      mocked_slack_web_client: mock.Mock,
  ) -> None:
    test_snapshot = "/path/to/mock/snapshot.jpg"
    mocked_motion_client.return_value.cleanup_snapshot.side_effect = \
        motion_client.MotionException("Boom!")

    client_instance.send_snapshot(test_snapshot)

    mocked_slack_web_client.return_value.files_upload_v2.\
        assert_called_once_with(
          channel=client_instance.channel_id,
          file=test_snapshot,
          title=client_instance.config.upload_file_title
        )
    mocked_slack_web_client.return_value.chat_postMessage.\
        assert_called_once_with(
          channel=client_instance.channel,
          text="An error occurred cleaning up this snapshot.",
        )
    mocked_motion_client.return_value.cleanup_snapshot.\
        assert_called_once_with(
          test_snapshot
        )
    assert mocked_logger.mock_calls == \
           [mock.call()] + \
           [
             mock.call().error("Failed to remove old motion snapshot!"),
           ]
