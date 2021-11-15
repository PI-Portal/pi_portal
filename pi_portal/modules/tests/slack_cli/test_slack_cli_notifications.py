"""Test Slack CLI Class."""

from pi_portal.modules.tests.slack_cli.fixtures.harness import (
  TestSlackCLIHarness,
)


class TestSlackCLI(TestSlackCLIHarness):
  """Test the SlackCLI class."""

  __test__ = True

  def test_notify_already_up(self):
    self.cli.notify_already_up()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Already running ..."
    )

  def test_notify_already_down(self):
    self.cli.notify_already_down()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Already stopped ..."
    )

  def test_notify_error(self):
    self.cli.notify_error()
    self.cli.slack_client.send_message.assert_called_once_with(
        "An internal error occurred ... you better take a look."
    )

  def test_notify_starting(self):
    self.cli.notify_starting()
    self.cli.slack_client.send_message.assert_called_once_with("Starting ...")

  def test_notify_stopping(self):
    self.cli.notify_stopping()
    self.cli.slack_client.send_message.assert_called_once_with(
        "Shutting down ..."
    )
