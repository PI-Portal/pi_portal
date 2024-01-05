"""Test the InstallerCommand class."""

from unittest import mock

from .. import installer
from ..bases import file_command
from ..mixins import state


class TestInstallerCommand:
  """Test the InstallerCommand class."""

  def check_click_echo(
      self,
      m_click: mock.Mock,
  ) -> None:
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

  def test_initialize__attributes(
      self,
      mocked_file_name: str,
      installer_command_instance: installer.InstallerCommand,
  ) -> None:
    assert installer_command_instance.file_name == mocked_file_name
    assert installer_command_instance.override is False

  def test_initialize__inheritance(
      self,
      installer_command_instance: installer.InstallerCommand,
  ) -> None:
    assert isinstance(installer_command_instance, file_command.FileCommandBase)
    assert isinstance(
        installer_command_instance, state.CommandManagedStateMixin
    )

  def test_invoke__no_override__confirmed__calls(
      self,
      installer_command_instance: installer.InstallerCommand,
      mocked_click: mock.Mock,
      mocked_file_name: str,
      mocked_installer: mock.Mock,
  ) -> None:
    mocked_click.confirm.return_value = True

    installer_command_instance.invoke()

    mocked_installer.assert_called_once_with(mocked_file_name)
    mocked_installer.return_value.install.assert_called_once_with()
    self.check_click_echo(mocked_click)
    mocked_click.confirm.assert_called_once_with(
        "Are you sure you want to proceed?"
    )

  def test_invoke____no_override__declined__calls(
      self,
      installer_command_instance: installer.InstallerCommand,
      mocked_installer: mock.Mock,
      mocked_click: mock.Mock,
  ) -> None:
    mocked_click.confirm.return_value = False

    installer_command_instance.invoke()

    mocked_installer.assert_not_called()
    self.check_click_echo(mocked_click)
    mocked_click.confirm.assert_called_once_with(
        "Are you sure you want to proceed?"
    )

  def test_invoke__override__calls(
      self,
      installer_command_instance: installer.InstallerCommand,
      mocked_click: mock.Mock,
      mocked_file_name: str,
      mocked_installer: mock.Mock,
  ) -> None:
    installer_command_instance.override = True
    mocked_click.confirm.return_value = True

    installer_command_instance.invoke()

    mocked_installer.assert_called_once_with(mocked_file_name)
    mocked_installer.return_value.install.assert_called_once_with()
    self.check_click_echo(mocked_click)
    mocked_click.confirm.assert_not_called()
