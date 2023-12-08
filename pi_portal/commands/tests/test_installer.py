"""Test the InstallerCommand class."""

from unittest import mock

from pi_portal.commands.bases.tests.fixtures import file_command_harness
from .. import installer


@mock.patch(installer.__name__ + ".click", mock.Mock())
class TestInstallerCommand(file_command_harness.FileCommandBaseTestHarness):
  """Test the InstallerCommand class.

  :param file_name: The path to a valid configuration file.
  """

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = installer.InstallerCommand

  def check_click_mock(self, m_click: mock.Mock) -> None:
    m_click.confirm.assert_called_once_with("Are you sure you want to proceed?")
    m_click.style.assert_called_once_with(
        "WARNING: This will overwrite existing configuration!",
        fg='yellow',
    )
    assert m_click.echo.mock_calls == \
        [
            mock.call(m_click.style()),
            mock.call(
                "This will affect existing configuration for the 'supervisord' "
                "and 'motion' services."
            ),
        ]

  @mock.patch(installer.__name__ + ".pi_portal_installer")
  def test_invoke(self, m_module: mock.Mock) -> None:

    with mock.patch(installer.__name__ + ".click") as m_click:
      m_click.confirm.return_value = True

      self.instance.invoke()

    m_module.Installer.assert_called_once_with(self.mock_file)
    m_module.Installer.return_value.install.assert_called_once_with()
    self.check_click_mock(m_click)

  @mock.patch(installer.__name__ + ".pi_portal_installer")
  def test_invoke__declined(self, m_module: mock.Mock) -> None:

    with mock.patch(installer.__name__ + ".click") as m_click:
      m_click.confirm.return_value = False

      self.instance.invoke()

    m_module.Installer.assert_not_called()
    self.check_click_mock(m_click)
