"""Test harness for the SlackCommandBase subclasses."""

from typing import Type
from unittest import TestCase, mock

from pi_portal.modules.integrations.slack.cli.commands.bases import command


class CommandBaseTestHarness(TestCase):
  """Test Harness for SlackCommandBase subclasses."""

  __test__ = False
  test_class: Type[command.SlackCommandBase]

  def setUp(self) -> None:
    self.mock_slack_client = mock.MagicMock()
    self.instance = self.test_class(self.mock_slack_client)
