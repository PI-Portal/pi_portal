"""Test the installation/configuration scripts."""

import os
import pathlib
from unittest import TestCase, mock

import pi_portal
from pi_portal import config
from pi_portal.modules import installer
from pi_portal.modules.tests.fixtures import environment

SCRIPT_DIRECTORY = pathlib.Path(
    os.path.dirname(__file__)
).parent.parent / "installation" / "scripts"


class TestLinux(TestCase):
  """Test the Linux utilities module."""

  @environment.patch
  @mock.patch(installer.__name__ + ".os.system")
  @mock.patch(installer.__name__ + ".os.chdir")
  def testUptime(self, m_chdir, m_system):
    mock_config_filename = "config.json"
    installer.installer(mock_config_filename)
    m_chdir.assert_called_once_with(SCRIPT_DIRECTORY)
    m_system.assert_called_once_with(
        "sudo bash install.sh "
        f"'{pi_portal.user_config['LOGZ_IO_CODE']}' "
        f"'{config.SUPERVISOR_SOCKET_PATH}' "
        f"'{mock_config_filename}'"
    )
