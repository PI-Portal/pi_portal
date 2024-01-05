"""CLI command to start the Installer."""

import click
from pi_portal.installation import installer as pi_portal_installer
from .bases import file_command
from .mixins import state


class InstallerCommand(
    file_command.FileCommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the Installer."""

  def __init__(
      self,
      file_name: str,
      override: bool,
  ) -> None:
    super().__init__(file_name)
    self.override = override

  def invoke(self) -> None:
    """Invoke the command."""

    click.echo(
        click.style(
            "WARNING: This will overwrite existing configuration!",
            fg='yellow',
        )
    )
    click.echo(
        "This will affect existing configuration for the 'supervisord' "
        "and 'motion' services."
    )
    if self.override or click.confirm('Are you sure you want to proceed?'):
      installer = pi_portal_installer.Installer(self.file_name)
      installer.install()
