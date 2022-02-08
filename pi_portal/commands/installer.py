"""CLI command to start the Installer."""

from pi_portal.modules.system import installer
from .bases import file_command


class InstallerCommand(file_command.FileCommandBase):
  """CLI command to start the Installer."""

  def invoke(self) -> None:
    """Invoke the command."""

    installer.installer(self.file_name)
