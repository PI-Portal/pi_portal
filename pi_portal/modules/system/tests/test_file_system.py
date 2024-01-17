"""Test the FileSystem class."""
from unittest import mock

from .. import file_system


class TestFileSystem:
  """Test the FileSystem class."""

  def test__intialize__attributes(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_file_path: str,
  ) -> None:
    assert file_system_instance.path == mocked_file_path

  def test__create__directory__calls_makedirs(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
  ) -> None:
    file_system_instance.create(directory=True)

    mocked_os.makedirs.assert_called_once_with(
        file_system_instance.path,
        exist_ok=True,
    )

  def test__create__file__writes_file(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
  ) -> None:
    file_system_instance.create()

    mocked_os.open.assert_called_once_with(
        file_system_instance.path,
        mocked_os.O_CREAT,
    )
    mocked_os.close.assert_called_once_with(mocked_os.open.return_value)

  def test__ownership__changes_ownership(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_shutil: mock.Mock,
  ) -> None:
    mock_user = "mock_user"
    mock_group = "mock_group"

    file_system_instance.ownership(mock_user, mock_group)

    mocked_shutil.chown.assert_called_once_with(
        file_system_instance.path,
        mock_user,
        mock_group,
    )

  def test__permissions__changes_permissions(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
  ) -> None:
    mock_permissions = "777"

    file_system_instance.permissions(mock_permissions)

    mocked_os.chmod.assert_called_once_with(
        file_system_instance.path,
        int(mock_permissions, 8),
    )
