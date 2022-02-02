"""Test the CommandBase class."""

from unittest import TestCase, mock

from pi_portal.modules.integrations.slack_cli import notifications
from pi_portal.modules.integrations.slack_cli.commands.bases import command


class ConcreteCLICommand(command.CommandBase):
  """A testable concrete instance of the CommandBase class."""

  def invoke(self) -> None:
    raise NotImplementedError


class TestSlackCLICommandBase(TestCase):
  """Test the CommandBase class."""

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    self.instance = ConcreteCLICommand(self.mock_slack_client)

  def test_instantiate(self) -> None:
    self.assertIsInstance(self.instance.notifier, notifications.SlackNotifier)
    self.assertEqual(self.instance.slack_client, self.mock_slack_client)

  def test_invoke(self) -> None:
    with self.assertRaises(NotImplementedError):
      self.instance.invoke()
