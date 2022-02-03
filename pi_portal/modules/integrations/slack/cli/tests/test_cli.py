"""Test Slack CLI utility methods."""

from unittest import TestCase

from pi_portal.modules.integrations.slack import cli


class TestGetAvailableCommands(TestCase):
  """Test the get_available_commands function."""

  def test_call(self) -> None:
    registered_commands = [
        'arm',
        'disarm',
        'help',
        'id',
        'restart',
        'snapshot',
        'status',
        'uptime',
    ]
    result = cli.get_available_commands()
    self.assertEqual(result, registered_commands)
