"""Test Slack CLI Class."""

from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.slack_cli import slack_cli


class TestSlackCLIHarness(TestCase):
  """Test harness for the SlackCLI class."""

  __test__ = False

  @mock_state.patch
  def setUp(self):
    self.slack_client = mock.MagicMock()
    self.cli = slack_cli.SlackCLI(client=self.slack_client)
    self.cli.supervisor_client = mock.MagicMock()
    self.cli.slack_client.motion_client = mock.MagicMock()
