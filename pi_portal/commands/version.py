"""CLI command to report the Pi Portal version."""

import click
import pkg_resources
from .bases import command


class VersionCommand(command.CommandBase):
  """CLI command to report the Pi Portal version."""

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(
        "Pi Portal Version: "
        f"{pkg_resources.get_distribution('pi_portal').version}",
    )
