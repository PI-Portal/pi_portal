"""Test the SlackClient class."""

from io import StringIO
from unittest import mock
from urllib.error import URLError

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.chat.bases.client import (
    ChatClientBase,
    ChatClientError,
)
from pi_portal.modules.integrations.chat.slack import client, config
from slack_sdk.errors import SlackClientError


@pytest.mark.usefixtures("test_state")
class TestSlackClient:
  """Test the SlackClient class."""

  def test_initialize__attributes(
      self,
      slack_client_instance: client.SlackClient,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    assert slack_client_instance.channel == (slack_user_config['SLACK_CHANNEL'])
    assert slack_client_instance.channel_id == (
        slack_user_config['SLACK_CHANNEL_ID']
    )

  def test_initialize__configuration(
      self,
      slack_client_instance: client.SlackClient,
  ) -> None:
    assert isinstance(
        slack_client_instance.configuration,
        config.SlackIntegrationConfiguration,
    )

  def test_initialize__slack_web_client__messages(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client: mock.Mock,
      mocked_slack_web_client_messages: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    assert slack_client_instance.web_client_messages == (
        mocked_slack_web_client_messages
    )
    assert mocked_slack_web_client.mock_calls[0] == mock.call(
        token=slack_user_config['SLACK_BOT_TOKEN'],
        timeout=30,
    )
    assert mocked_slack_web_client.call_count == 2

  def test_initialize__slack_web_client__files(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client: mock.Mock,
      mocked_slack_web_client_files: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    assert slack_client_instance.web_client_files == (
        mocked_slack_web_client_files
    )
    assert mocked_slack_web_client.mock_calls[1] == mock.call(
        token=slack_user_config['SLACK_BOT_TOKEN'],
        timeout=slack_user_config["SLACK_FILE_TRANSFER_TIMEOUT"],
    )
    assert mocked_slack_web_client.call_count == 2

  def test_initialize__inheritance(
      self,
      slack_client_instance: client.SlackClient,
  ) -> None:
    assert isinstance(
        slack_client_instance,
        client.SlackClient,
    )
    assert isinstance(
        slack_client_instance,
        ChatClientBase,
    )

  def test_send_message__success__calls_slack_client(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_messages: mock.Mock,
  ) -> None:
    test_message = "test message"

    slack_client_instance.send_message(test_message)

    mocked_slack_web_client_messages.chat_postMessage.\
        assert_called_once_with(
          channel=slack_client_instance.channel,
          text=test_message,
        )

  def test_send_message__success__logging(
      self,
      slack_client_instance: client.SlackClient,
      mocked_stream: StringIO,
  ) -> None:
    test_message = "test message"

    slack_client_instance.send_message(test_message)

    assert mocked_stream.getvalue() == ""

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_message__vary_exception__retries_slack_client__raises_exception(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_messages: mock.Mock,
      exception: Exception,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client_messages.chat_postMessage.side_effect = exception
    expected_client_call = mock.call(
        channel=slack_client_instance.channel,
        text=test_message,
    )
    expected_calls = [expected_client_call
                     ] * (slack_client_instance.message_retries)

    with pytest.raises(ChatClientError):
      slack_client_instance.send_message(test_message)

    assert mocked_slack_web_client_messages.chat_postMessage.mock_calls == (
        expected_calls
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_message__vary_exception__logging(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_messages: mock.Mock,
      mocked_stream: StringIO,
      exception: Exception,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client_messages.chat_postMessage.side_effect = exception

    with pytest.raises(ChatClientError):
      slack_client_instance.send_message(test_message)

    assert mocked_stream.getvalue() == (
        f"WARNING - Retrying failed message: '{test_message}' !\n" *
        slack_client_instance.message_retries
    ) + f"ERROR - Failed to send message: '{test_message}' !\n"

  def test_send_file__success__calls_slack_client(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_files: mock.Mock,
  ) -> None:
    test_file = "/path/to/mock/file.txt"
    test_file_description = "Just a test file."

    slack_client_instance.send_file(test_file, test_file_description)

    mocked_slack_web_client_files.files_upload_v2.\
        assert_called_once_with(
            channel=slack_client_instance.channel_id,
            file=test_file,
            title=test_file_description,
        )

  def test_send_file__success__logging(
      self,
      slack_client_instance: client.SlackClient,
      mocked_stream: StringIO,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."

    slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_stream.getvalue() == (
        f"DEBUG - Starting file transfer: '{test_file_path}' ...\n"
        f"DEBUG - File transfer: '{test_file_path}' complete !\n"
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_file__vary_exception__raises_exception(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_files: mock.Mock,
      exception: Exception,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    mocked_slack_web_client_files.files_upload_v2.side_effect = exception

    with pytest.raises(ChatClientError):
      slack_client_instance.send_file(test_file_path, test_file_description)

    mocked_slack_web_client_files.files_upload_v2.assert_called_once_with(
        channel=slack_client_instance.channel_id,
        file=test_file_path,
        title=test_file_description,
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_file__vary_exception__logging(
      self,
      slack_client_instance: client.SlackClient,
      mocked_slack_web_client_files: mock.Mock,
      mocked_stream: StringIO,
      exception: Exception,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    mocked_slack_web_client_files.files_upload_v2.side_effect = exception

    with pytest.raises(ChatClientError):
      slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_stream.getvalue() == (
        f"DEBUG - Starting file transfer: '{test_file_path}' ...\n"
        f"ERROR - Failed to transfer file: '{test_file_path}' !\n"
    )
