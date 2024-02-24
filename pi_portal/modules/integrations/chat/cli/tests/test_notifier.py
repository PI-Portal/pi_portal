"""Test the ChatCLINotifier Class."""

from unittest import mock

from pi_portal.modules.integrations.chat.cli.notifier import ChatCLINotifier


class TestChatCLI:
  """Test the ChatCLINotifier Class."""

  def test_initialize__attributes(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    assert cli_notifier_instance.chat_client == mocked_chat_client

  def test_notify_already_start__send_message(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    cli_notifier_instance.notify_already_start()

    mocked_chat_client.send_message.assert_called_once_with(
        "Already running ..."
    )

  def test_notify_already_stop(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    cli_notifier_instance.notify_already_stop()

    mocked_chat_client.send_message.assert_called_once_with(
        "Already stopped ..."
    )

  def test_notify_error(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    cli_notifier_instance.notify_error()

    mocked_chat_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_notify_start(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    cli_notifier_instance.notify_start()

    mocked_chat_client.send_message.assert_called_once_with("Starting ...")

  def test_notify_stop(
      self,
      cli_notifier_instance: ChatCLINotifier,
      mocked_chat_client: mock.Mock,
  ) -> None:
    cli_notifier_instance.notify_stop()

    mocked_chat_client.send_message.assert_called_once_with("Shutting down ...")
