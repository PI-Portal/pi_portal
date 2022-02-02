"""Test the installer module."""

import os
import pathlib
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.system import installer


class TestInstaller(TestCase):
  """Test the installer function."""

  script_directory = pathlib.Path(
      os.path.dirname(__file__)
  ).parent.parent / "installation" / "scripts"

  mock_config_file_content = {
      'LOGZ_IO_CODE': "Mock Log Code"
  }

  @mock_state.patch
  @mock.patch(installer.__name__ + ".os.system")
  @mock.patch(installer.__name__ + ".os.chdir")
  @mock.patch(installer.__name__ + ".user_config.UserConfiguration")
  def test_installer(
      self,
      m_config: mock.Mock,
      m_chdir: mock.Mock,
      m_system: mock.Mock,
  ) -> None:
    m_config.return_value.user_config = self.mock_config_file_content
    mock_config_filename = "mock.config.json"

    installer.installer(mock_config_filename)

    m_chdir.assert_called_once_with(self.script_directory)
    m_system.assert_called_once_with(
        "sudo bash install.sh "
        f"'{self.mock_config_file_content['LOGZ_IO_CODE']}' "
        f"'{config.SUPERVISOR_SOCKET_PATH}' "
        f"'{os.path.abspath(mock_config_filename)}'"
    )
