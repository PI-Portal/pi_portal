"""Test Slack CLI Class initialization state."""

from unittest import TestCase, mock

from pi_portal.modules import slack_cli
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.system import supervisor


class TestSlackCLI(TestCase):
  """Test the SlackCLI class initialize state."""

  def setUp(self):
    self.slack_client = mock.Mock()

  @mock_state.patch
  def test_initialize(self):
    cli = slack_cli.SlackCLI(client=self.slack_client)
    self.assertEqual(cli.prefix, "command_")
    self.assertEqual(cli.slack_client, self.slack_client)
    self.assertIsInstance(cli.supervisor_client, supervisor.SupervisorClient)
