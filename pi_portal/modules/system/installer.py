"""The installation/configuration scripts."""

import os
import pathlib

from pi_portal import config
from pi_portal.modules.configuration import config_file


def installer(user_config_file: str):
  """Run the onboard installer.

  :param user_config_file: The path to user's config file.
  """

  configuration = config_file.UserConfiguration()
  user_config = configuration.load(user_config_file)
  absolute_path = os.path.abspath(user_config_file)

  script_directory = pathlib.Path(
      os.path.dirname(__file__)
  ).parent / "installation" / "scripts"

  os.chdir(script_directory)
  os.system(  # nosec
      "sudo bash install.sh "
      f"'{user_config['LOGZ_IO_CODE']}' "
      f"'{config.SUPERVISOR_SOCKET_PATH}' "
      f"'{absolute_path}'"
  )
