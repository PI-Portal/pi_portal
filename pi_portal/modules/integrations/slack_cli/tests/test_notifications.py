"""Test the SlackNotifier Class."""

from typing import cast
from unittest import TestCase, mock

from pi_portal.modules.integrations.slack_cli.notifications import SlackNotifier


class TestSlackCLI(TestCase):
  """Test the SlackNotifier Class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    self.instance = SlackNotifier(self.mock_slack_client)

  def _mocked_client(self) -> mock.Mock:
    return cast(mock.Mock, self.instance.slack_client)

  def test_initialize(self) -> None:
    self.assertEqual(self.instance.slack_client, self.mock_slack_client)

  def test_notify_already_start(self) -> None:
    self.instance.notify_already_start()
    self._mocked_client(
    ).send_message.assert_called_once_with("Already running ...")

  def test_notify_already_stop(self) -> None:
    self.instance.notify_already_stop()
    self._mocked_client(
    ).send_message.assert_called_once_with("Already stopped ...")

  def test_notify_error(self) -> None:
    self.instance.notify_error()
    self._mocked_client().send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_notify_start(self) -> None:
    self.instance.notify_start()
    self._mocked_client().send_message.assert_called_once_with("Starting ...")

  def test_notify_stop(self) -> None:
    self.instance.notify_stop()
    self._mocked_client(
    ).send_message.assert_called_once_with("Shutting down ...")
