"""Test the FileSystem class."""
from unittest import mock

from .. import file_system


class TestFileSystem:
  """Test the FileSystem class."""

  def test_intialize__attributes(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_file_path: str,
  ) -> None:
    assert file_system_instance.path == mocked_file_path
    assert file_system_instance.poll_interval == 0.5

  def test_create__directory__calls_makedirs(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
  ) -> None:
    file_system_instance.create(directory=True)

    mocked_os.makedirs.assert_called_once_with(
        file_system_instance.path,
        exist_ok=True,
    )

  def test_create__file__writes_file(
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

  def test_ownership__changes_ownership(
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

  def test_permissions__changes_permissions(
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

  def test_wait_until_exists__calls_exists(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
  ) -> None:
    mocked_os.path.exists.side_effect = [False, False, True]

    file_system_instance.wait_until_exists()

    assert mocked_os.path.exists.mock_calls == [
        mock.call(file_system_instance.path),
    ] * 3

  def test_wait_until_exists__calls_sleep(
      self,
      file_system_instance: file_system.FileSystem,
      mocked_os: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    mocked_os.path.exists.side_effect = [False, False, True]

    file_system_instance.wait_until_exists()

    assert mocked_sleep.mock_calls == [
        mock.call(file_system_instance.poll_interval),
    ] * 2
