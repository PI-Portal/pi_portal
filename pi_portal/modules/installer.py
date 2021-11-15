"""The installation/configuration scripts."""

import os
import pathlib

import pi_portal
from pi_portal import config


def installer(config_file: str):
  """Run the onboard installer."""

  script_directory = pathlib.Path(
      os.path.dirname(__file__)
  ).parent / "installation" / "scripts"

  os.chdir(script_directory)
  os.system(  # nosec
      "sudo bash install.sh "
      f"'{pi_portal.user_config['LOGZ_IO_CODE']}' "
      f"'{config.SUPERVISOR_SOCKET_PATH}' "
      f"'{config_file}'"
  )
