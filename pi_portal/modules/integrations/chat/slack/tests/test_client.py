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
from .conftest import TypeSlackClientCreator


@pytest.mark.usefixtures("test_state")
class TestSlackClient:
  """Test the SlackClient class."""

  @pytest.mark.parametrize("propagate_exceptions", [True, False])
  def test_initialize__vary_propagate__attributes(
      self,
      slack_client_creator: TypeSlackClientCreator,
      test_state: state.State,
      propagate_exceptions: bool,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    slack_client_instance = slack_client_creator(propagate_exceptions)

    assert slack_client_instance.channel == (slack_user_config['SLACK_CHANNEL'])
    assert slack_client_instance.channel_id == (
        slack_user_config['SLACK_CHANNEL_ID']
    )
    assert slack_client_instance.propagate_exceptions is propagate_exceptions

  def test_initialize__no_propagate__configuration(
      self,
      slack_client_creator: TypeSlackClientCreator,
  ) -> None:
    slack_client_instance = slack_client_creator(False)

    assert isinstance(
        slack_client_instance.configuration,
        config.SlackIntegrationConfiguration,
    )

  def test_initialize__no_propagate__slack_web_client__chat(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client: mock.Mock,
      mocked_slack_web_client_chat: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    slack_client_instance = slack_client_creator(False)

    assert slack_client_instance.web_chat == mocked_slack_web_client_chat
    assert mocked_slack_web_client.mock_calls[0] == mock.call(
        token=slack_user_config['SLACK_BOT_TOKEN'],
        timeout=30,
    )
    assert mocked_slack_web_client.call_count == 2

  def test_initialize__no_propagate__slack_web_client__files(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client: mock.Mock,
      mocked_slack_web_client_files: mock.Mock,
      test_state: state.State,
  ) -> None:
    slack_user_config = test_state.user_config["CHAT"]["SLACK"]

    slack_client_instance = slack_client_creator(False)

    assert slack_client_instance.web_files == mocked_slack_web_client_files
    assert mocked_slack_web_client.mock_calls[1] == mock.call(
        token=slack_user_config['SLACK_BOT_TOKEN'],
        timeout=300,
    )
    assert mocked_slack_web_client.call_count == 2

  def test_initialize__no_propagate__inheritance(
      self,
      slack_client_creator: TypeSlackClientCreator,
  ) -> None:
    slack_client_instance = slack_client_creator(False)

    assert isinstance(
        slack_client_instance,
        client.SlackClient,
    )
    assert isinstance(
        slack_client_instance,
        ChatClientBase,
    )

  def test_send_message__no_propagate__success__calls_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_chat: mock.Mock,
  ) -> None:
    test_message = "test message"
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_message(test_message)

    mocked_slack_web_client_chat.chat_postMessage.\
        assert_called_once_with(
          channel=slack_client_instance.channel,
          text=test_message,
        )

  def test_send_message__no_propagate__success__logging(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_stream: StringIO,
  ) -> None:
    test_message = "test message"
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_message(test_message)

    assert mocked_stream.getvalue() == ""

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_message__no_propagate__vary_exception__retries_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_chat: mock.Mock,
      exception: Exception,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client_chat.chat_postMessage.side_effect = exception
    slack_client_instance = slack_client_creator(False)
    expected_client_call = mock.call(
        channel=slack_client_instance.channel,
        text=test_message,
    )
    expected_calls = [expected_client_call] * slack_client_instance.retries

    slack_client_instance.send_message(test_message)

    assert mocked_slack_web_client_chat.chat_postMessage.mock_calls == (
        expected_calls
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_message__with_propagate__vary_exception__retries_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_chat: mock.Mock,
      exception: Exception,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client_chat.chat_postMessage.side_effect = exception
    slack_client_instance = slack_client_creator(True)
    expected_client_call = mock.call(
        channel=slack_client_instance.channel,
        text=test_message,
    )
    expected_calls = [expected_client_call] * slack_client_instance.retries

    with pytest.raises(ChatClientError):
      slack_client_instance.send_message(test_message)

    assert mocked_slack_web_client_chat.chat_postMessage.mock_calls == (
        expected_calls
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_message__no_propagate__vary_exception__logging(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_chat: mock.Mock,
      mocked_stream: StringIO,
      exception: Exception,
  ) -> None:
    test_message = "test message"
    mocked_slack_web_client_chat.chat_postMessage.side_effect = exception
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_message(test_message)

    assert mocked_stream.getvalue() == (
        f"WARNING - Retrying failed message: '{test_message}' !\n" *
        slack_client_instance.retries
    ) + f"ERROR - Failed to send message: '{test_message}' !\n"

  def test_send_file__no_propagate__success__calls_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_files: mock.Mock,
  ) -> None:
    test_file = "/path/to/mock/file.txt"
    test_file_description = "Just a test file."
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_file(test_file, test_file_description)

    mocked_slack_web_client_files.files_upload_v2.\
        assert_called_once_with(
            channel=slack_client_instance.channel_id,
            file=test_file,
            title=test_file_description,
        )

  def test_send_file__no_propagate__success__logging(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_stream: StringIO,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_stream.getvalue() == ""

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_file__no_propagate__vary_exception__retries_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_files: mock.Mock,
      exception: Exception,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    mocked_slack_web_client_files.files_upload_v2.side_effect = exception
    slack_client_instance = slack_client_creator(False)
    expected_client_call = mock.call(
        channel=slack_client_instance.channel_id,
        file=test_file_path,
        title=test_file_description,
    )
    expected_calls = [expected_client_call] * slack_client_instance.retries

    slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_slack_web_client_files.files_upload_v2.mock_calls == (
        expected_calls
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_file__with_propagate__vary_exception__retries_slack_client(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_files: mock.Mock,
      exception: Exception,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    mocked_slack_web_client_files.files_upload_v2.side_effect = exception
    slack_client_instance = slack_client_creator(True)
    expected_client_call = mock.call(
        channel=slack_client_instance.channel_id,
        file=test_file_path,
        title=test_file_description,
    )
    expected_calls = [expected_client_call] * slack_client_instance.retries

    with pytest.raises(ChatClientError):
      slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_slack_web_client_files.files_upload_v2.mock_calls == (
        expected_calls
    )

  @pytest.mark.parametrize(
      "exception", [
          SlackClientError(),
          URLError(reason="Mock Error"),
      ]
  )
  def test_send_file__no_propagate__vary_exception__logging(
      self,
      slack_client_creator: TypeSlackClientCreator,
      mocked_slack_web_client_files: mock.Mock,
      mocked_stream: StringIO,
      exception: Exception,
  ) -> None:
    test_file_path = "/var/lib/some/file.txt"
    test_file_description = "Just a test file."
    mocked_slack_web_client_files.files_upload_v2.side_effect = exception
    slack_client_instance = slack_client_creator(False)

    slack_client_instance.send_file(test_file_path, test_file_description)

    assert mocked_stream.getvalue() == (
        f"WARNING - Retrying failed file transmission: '{test_file_path}' !\n" *
        slack_client_instance.retries
    ) + f"ERROR - Failed to send file: '{test_file_path}' !\n"
