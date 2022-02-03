"""Test the SlackCommandBase class."""

from unittest import TestCase, mock

from pi_portal.modules.integrations.slack.cli import notifier
from pi_portal.modules.integrations.slack.cli.commands.bases import command


class ConcreteCLICommand(command.SlackCommandBase):
  """A testable concrete instance of the SlackCommandBase class."""

  def invoke(self) -> None:
    raise NotImplementedError


class TestSlackCLICommandBase(TestCase):
  """Test the SlackCommandBase class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    self.instance = ConcreteCLICommand(self.mock_slack_client)

  def test_instantiate(self) -> None:
    self.assertIsInstance(self.instance.notifier, notifier.SlackCLINotifier)
    self.assertEqual(self.instance.slack_client, self.mock_slack_client)

  def test_invoke(self) -> None:
    with self.assertRaises(NotImplementedError):
      self.instance.invoke()
