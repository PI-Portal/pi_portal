"""Test the VersionCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_user import version
from pi_portal.modules.python.metadata import metadata_version


class TestVersionCommand:
  """Test the VersionCommand class."""

  def test_initialize__inheritance(
      self,
      version_command_instance: version.VersionCommand,
  ) -> None:
    assert isinstance(version_command_instance, command.CommandBase)

  def test_invoke__calls(
      self,
      version_command_instance: version.VersionCommand,
      mocked_click: mock.Mock,
  ) -> None:
    expected_version = metadata_version('pi_portal')

    version_command_instance.invoke()

    mocked_click.echo.assert_called_once_with(
        f"Pi Portal Version: {expected_version}"
    )
