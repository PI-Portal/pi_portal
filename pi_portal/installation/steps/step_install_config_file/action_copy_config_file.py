"""CreatePiPortalFoldersAction class."""

import shutil

from pi_portal import config
from pi_portal.installation.actions.bases.base_action import ActionBase
from pi_portal.modules.system import file_system


class CopyPiPortalUserConfigAction(ActionBase):
  """Copy the user's configuration file into place."""

  config_file_path: str

  def invoke(self) -> None:
    """Copy the user's configuration file into place."""

    try:
      shutil.copy(self.config_file_path, config.PATH_USER_CONFIG)
    except shutil.SameFileError:
      pass

    self.log.info("Setting permissions on the user's configuration file ...")
    fs = file_system.FileSystem(config.PATH_USER_CONFIG)
    fs.ownership(config.PI_PORTAL_USER, config.PI_PORTAL_USER)
    fs.permissions("600")
    self.log.info("Done setting permissions on the user's configuration file.")
