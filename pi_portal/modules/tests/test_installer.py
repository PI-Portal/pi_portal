"""Test the installation/configuration scripts."""

import os
import pathlib
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules import installer
from pi_portal.modules.tests.fixtures import mock_state

SCRIPT_DIRECTORY = pathlib.Path(
    os.path.dirname(__file__)
).parent.parent / "installation" / "scripts"

MOCK_CONFIG_FILE_CONTENT = {
    'LOGZ_IO_CODE': "Mock Log Code"
}


class TestInstaller(TestCase):
  """Test the installation/configuration module."""

  @mock_state.patch
  @mock.patch(installer.__name__ + ".os.system")
  @mock.patch(installer.__name__ + ".os.chdir")
  @mock.patch(installer.__name__ + ".config_file.UserConfiguration")
  def test_installer(self, m_config, m_chdir, m_system):
    m_config.return_value.load.return_value = MOCK_CONFIG_FILE_CONTENT
    mock_config_filename = "mock.config.json"

    installer.installer(mock_config_filename)

    m_chdir.assert_called_once_with(SCRIPT_DIRECTORY)
    m_system.assert_called_once_with(
        "sudo bash install.sh "
        f"'{MOCK_CONFIG_FILE_CONTENT['LOGZ_IO_CODE']}' "
        f"'{config.SUPERVISOR_SOCKET_PATH}' "
        f"'{os.path.abspath(mock_config_filename)}'"
    )
