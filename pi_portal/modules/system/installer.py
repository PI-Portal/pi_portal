"""Pi Portal installation utilities."""

import os
import pathlib

from pi_portal import config
from pi_portal.modules.configuration import user_config


def installer(user_config_file: str) -> None:
  """Run the onboard installer.

  :param user_config_file: The path to the end user's config file.
  """

  configuration = user_config.UserConfiguration()
  configuration.load(user_config_file)
  absolute_path = os.path.abspath(user_config_file)

  script_directory = pathlib.Path(
      os.path.dirname(__file__)
  ).parent.parent / "installation" / "scripts"

  os.chdir(script_directory)
  os.system(  # nosec
      "sudo bash install.sh "
      f"'{configuration.user_config['LOGZ_IO_CODE']}' "
      f"'{config.PATH_SUPERVISOR_SOCKET}' "
      f"'{absolute_path}'"
  )
