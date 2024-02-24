"""Test chat CLI utility methods."""

from pi_portal.modules.integrations.chat import cli


class TestGetAvailableCommands:
  """Test the get_available_commands function."""

  expected_commands = [
      'arm',
      'disarm',
      'help',
      'id',
      'restart',
      'snapshot',
      'status',
      'temp',
      'uptime',
  ]

  def test_call(self) -> None:
    result = cli.get_available_commands()

    assert result == self.expected_commands
