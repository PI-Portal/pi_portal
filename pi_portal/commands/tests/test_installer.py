"""Test the InstallerCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import file_command_harness
from .. import installer


class TestInstallerCommand(file_command_harness.FileCommandBaseTestHarness):
  """Test the InstallerCommand class.

  :param file_name: The path to a valid configuration file.
  """

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = installer.InstallerCommand

  @mock.patch(installer.__name__ + ".installer")
  def test_invoke(self, m_module: mock.Mock) -> None:
    self.instance.invoke()
    m_module.installer.assert_called_once_with(self.mock_file)
