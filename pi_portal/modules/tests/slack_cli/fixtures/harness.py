"""Test Slack CLI Class."""

from unittest import TestCase, mock

from pi_portal.modules import slack_cli
from pi_portal.modules.tests.fixtures import mock_state


class TestSlackCLIHarness(TestCase):
  """Test harness for the SlackCLI class."""

  __test__ = False

  @mock_state.patch
  def setUp(self):
    self.slack_client = mock.MagicMock()
    self.cli = slack_cli.SlackCLI(client=self.slack_client)
    self.cli.supervisor_client = mock.MagicMock()
    self.cli.slack_client.motion_client = mock.MagicMock()
