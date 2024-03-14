"""CreatePiPortalFoldersAction class."""

import os

from pi_portal.installation.actions.bases.base_action import ActionBase


class EnsureRootAction(ActionBase):
  """Ensure the installer is running as root."""

  insufficient_privileges_msg: str = \
      "The pi_portal configuration installer must be run as root!"

  def invoke(self) -> None:
    """Copy the user's configuration file into place."""

    if os.geteuid() != 0:
      self.log.error("This installer must be run as root!")
      raise PermissionError(self.insufficient_privileges_msg)
