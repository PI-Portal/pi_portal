"""CLI command to report the Pi Portal version."""

import click
from pi_portal.cli_commands.bases import command
from pi_portal.modules.python.metadata import metadata_version


class VersionCommand(command.CommandBase):
  """CLI command to report the Pi Portal version."""

  def invoke(self) -> None:
    """Invoke the command."""
    version = metadata_version('pi_portal')

    click.echo(f"Pi Portal Version: {version}")
