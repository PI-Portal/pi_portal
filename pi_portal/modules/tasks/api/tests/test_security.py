"""Test the SocketSecurity class."""

import os
from typing import List
from unittest import mock

from pi_portal import config
from .. import security


class TestSocketSecurity:
  """Test the SocketSecurity class."""

  def test_initialize__attributes(
      self,
      socket_security_instance: security.SocketSecurity,
  ) -> None:
    assert socket_security_instance.polling_interval == 0.5
    assert socket_security_instance.socket_permissions == "600"
    assert socket_security_instance.socket_dir_permissions == "700"

  def test_initialize__attributes__file_system(
      self,
      socket_security_instance: security.SocketSecurity,
      mocked_file_system: mock.Mock,
      mocked_file_system_objects: List[mock.Mock],
  ) -> None:
    assert mocked_file_system.call_count == 2
    assert mocked_file_system.mock_calls[0] == \
        mock.call(config.PI_PORTAL_TASK_MANAGER_SOCKET)
    assert socket_security_instance.fs_socket == \
        mocked_file_system_objects[0]
    assert mocked_file_system.mock_calls[1] == \
        mock.call(os.path.dirname(config.PI_PORTAL_TASK_MANAGER_SOCKET))
    assert socket_security_instance.fs_socket_dir == \
        mocked_file_system_objects[1]

  def test_initialize__file_system__fs_socket(
      self,
      mocked_file_system_objects: List[mock.Mock],
  ) -> None:
    mocked_file_system_objects[0].assert_not_called()

  def test_initialize__file_system__fs_socket_dir(
      self,
      socket_security_instance: security.SocketSecurity,
      mocked_file_system_objects: List[mock.Mock],
  ) -> None:
    mocked_file_system_objects[1].create.assert_called_once_with(directory=True)
    mocked_file_system_objects[1].permissions.assert_called_once_with(
        socket_security_instance.socket_dir_permissions
    )

  def test_rewrite_permissions__two_intervals__calls_os_path_exists(
      self,
      socket_security_instance: security.SocketSecurity,
      mocked_file_system_objects: List[mock.Mock],
      mocked_os_path_exists: mock.Mock,
  ) -> None:
    mocked_os_path_exists.side_effect = [False, True]

    socket_security_instance.rewrite_permissions()

    assert mocked_os_path_exists.mock_calls == \
        [mock.call(mocked_file_system_objects[0].path)] * 2

  def test_rewrite_permissions__two_intervals__calls_sleep(
      self,
      socket_security_instance: security.SocketSecurity,
      mocked_os_path_exists: mock.Mock,
      mocked_sleep: mock.Mock,
  ) -> None:
    mocked_os_path_exists.side_effect = [False, True]

    socket_security_instance.rewrite_permissions()

    assert mocked_sleep.mock_calls == [
        mock.call(socket_security_instance.polling_interval)
    ]

  def test_rewrite_permissions__two_intervals__writes_permissions(
      self,
      socket_security_instance: security.SocketSecurity,
      mocked_file_system_objects: List[mock.Mock],
      mocked_os_path_exists: mock.Mock,
  ) -> None:
    mocked_os_path_exists.side_effect = [False, True]

    socket_security_instance.rewrite_permissions()

    mocked_file_system_objects[0].permissions.assert_called_once_with(
        socket_security_instance.socket_permissions
    )
    assert mocked_file_system_objects[1].permissions.mock_calls == [
        mock.call(socket_security_instance.socket_dir_permissions)
    ] * 2
