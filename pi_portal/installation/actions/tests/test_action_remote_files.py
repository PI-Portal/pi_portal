"""Test the RemoteFilesAction class."""

import logging
from io import StringIO
from typing import List, Type
from unittest import mock

import pytest
from pi_portal.modules.integrations.network import http
from pi_portal.modules.python.mock import CallType
from pi_portal.modules.system import file_security
from ..action_remote_files import (
    RemoteFile,
    RemoteFileDownloadError,
    RemoteFilesAction,
)
from ..bases import base_action


class TestRemoteFilesAction:
  """Test the RemoteFilesAction class."""

  def build_logging__successful(
      self,
      remote_files: List[RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "INFO - Download: "
                      f"'{remote_file.url}' -> '{remote_file.target}' ..."
                  ),
                  (
                      "INFO - Download: Successfully saved "
                      f"'{remote_file.target}' !"
                  ),
              ]
          ) + "\n"
      )
    return expected_logs

  def build_logging__failed_http_get(
      self,
      remote_files: List[RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "INFO - Download: "
                      f"'{remote_file.url}' -> '{remote_file.target}' ..."
                  ),
                  (
                      "ERROR - Download: Unable to retrieve remote file "
                      f"from '{remote_file.url}' !"
                  )
              ]
          ) + "\n"
      )
    return expected_logs

  def build_logging__failed_security_hash(
      self,
      remote_files: List[RemoteFile],
  ) -> str:
    expected_logs = "\n".join(
        [
            (
                "INFO - Download: "
                f"'{remote_files[0].url}' -> '{remote_files[0].target}' ..."
            ),
            (
                "ERROR - Download: Unexpected hash value for file "
                f"downloaded from '{remote_files[0].url}' !"
            )
        ]
    ) + "\n"
    return expected_logs

  def build_logging__failed_filesystem_operation(
      self,
      remote_files: List[RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "INFO - Download: "
                      f"'{remote_file.url}' -> '{remote_file.target}' ..."
                  ),
              ]
          ) + "\n"
      )
    return expected_logs

  def build_logging__failed_file_system_calls(
      self,
      remote_files: List[RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "INFO - Download: "
                      f"'{remote_file.url}' -> "
                      f"'{remote_file.target}' ..."
                  ),
              ]
          ) + "\n"
      )
    return expected_logs

  def build_mocked_file_security_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> List[CallType]:
    expected_file_security_calls: List[CallType] = []
    for remote_file in concrete_action_remote_files_instance.remote_files:
      expected_file_security_calls += [
          mock.call(remote_file.target),
          mock.call().sha256(remote_file.sha256),
      ]
    return expected_file_security_calls

  def build_mocked_file_system_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> List[CallType]:
    expected_fs_calls: List[CallType] = []
    for remote_file in concrete_action_remote_files_instance.remote_files:
      expected_fs_calls += [
          mock.call(remote_file.target),
          mock.call().ownership(
              remote_file.user,
              remote_file.group,
          ),
          mock.call().permissions(remote_file.permissions),
      ]
    return expected_fs_calls

  def build_mocked_http_client_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> List[CallType]:
    expected_http_client_calls: List[CallType] = []
    for remote_file in concrete_action_remote_files_instance.remote_files:
      expected_http_client_calls += [
          mock.call(concrete_action_remote_files_instance.log),
          mock.call().get(remote_file.url, remote_file.target),
      ]
    return expected_http_client_calls

  def test_initialize__class__attributes(
      self,
      concrete_action_remote_files_class: Type[RemoteFilesAction],
  ) -> None:
    assert concrete_action_remote_files_class.fail_fast is True
    assert concrete_action_remote_files_class.worker_count == 4

  def test_initialize__instance__attributes(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> None:
    assert isinstance(concrete_action_remote_files_instance.log, logging.Logger)
    # Serially during testing
    assert concrete_action_remote_files_instance.worker_count == 1
    assert concrete_action_remote_files_instance.fail_fast is False

  def test_initialize__inheritance(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> None:
    assert isinstance(
        concrete_action_remote_files_instance,
        base_action.ActionBase,
    )

  def test_initialize__remote_files(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
  ) -> None:
    assert len(concrete_action_remote_files_instance.remote_files) == 2
    for remote_file in concrete_action_remote_files_instance.remote_files:
      assert isinstance(
          remote_file,
          RemoteFile,
      )

  def test_invoke__success__logging(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_stream: StringIO,
  ) -> None:
    expected_log_messages = \
        self.build_logging__successful(
          concrete_action_remote_files_instance.remote_files
        )

    concrete_action_remote_files_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__success__http_client_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_http_client: mock.Mock,
  ) -> None:
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_action_remote_files_instance
        )

    concrete_action_remote_files_instance.invoke()

    assert mocked_http_client.mock_calls == \
           expected_http_client_calls

  def test_invoke__success__file_security_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
  ) -> None:
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_action_remote_files_instance
        )

    concrete_action_remote_files_instance.invoke()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls

  def test_invoke__success__file_system_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_action_remote_files_instance
    )

    concrete_action_remote_files_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test_invoke__download_failure__logging(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_http_client: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_log_messages = self.build_logging__failed_http_get(
        concrete_action_remote_files_instance.remote_files[0:1]
    )
    expected_log_messages += self.build_logging__successful(
        concrete_action_remote_files_instance.remote_files[1:]
    )

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__download_failure__http_client_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_action_remote_files_instance
        )

    with pytest.raises(RemoteFileDownloadError) as exc:
      concrete_action_remote_files_instance.invoke()

    assert mocked_http_client.mock_calls == expected_http_client_calls
    assert str(exc.value) == \
        concrete_action_remote_files_instance.remote_files[0].url

  def test_invoke__download_failure__file_security_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_action_remote_files_instance
        )[2:]

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls

  def test_invoke__download_failure__file_system_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_system: mock.Mock,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_action_remote_files_instance
    )[3:]

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_system.mock_calls == \
        expected_fs_calls

  def test_invoke__file_system_failure__logging(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_log_messages = \
        self.build_logging__failed_file_system_calls(
          concrete_action_remote_files_instance.remote_files[0:1]
        )
    expected_log_messages += \
        self.build_logging__failed_filesystem_operation(
          concrete_action_remote_files_instance.remote_files[1:]
        )

    with pytest.raises(OSError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__file_system_failure__http_client_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_system: mock.Mock,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_action_remote_files_instance
        )

    with pytest.raises(OSError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_http_client.mock_calls == expected_http_client_calls

  def test_invoke__file_system_failure__file_security_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
      mocked_file_system: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_action_remote_files_instance
        )

    with pytest.raises(OSError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_security.mock_calls == \
           expected_file_security_calls

  def test_invoke__file_system_failure__file_system_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_system: mock.Mock,
  ) -> None:
    mocked_file_system.return_value.permissions.side_effect = OSError
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_action_remote_files_instance
    )

    with pytest.raises(OSError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls

  def test_invoke__file_security_failure__logging(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_log_messages = \
        self.build_logging__failed_security_hash(
          concrete_action_remote_files_instance.remote_files[0:1]
        )
    expected_log_messages += \
        self.build_logging__successful(
          concrete_action_remote_files_instance.remote_files[1:]
        )

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_stream.getvalue() == expected_log_messages

  def test_invoke__file_security_failure__http_client_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
      mocked_http_client: mock.Mock,
  ) -> None:
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_action_remote_files_instance
        )

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_http_client.mock_calls == expected_http_client_calls

  def test_invoke__file_security_failure__file_security_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
  ) -> None:
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_action_remote_files_instance
        )

    with pytest.raises(RemoteFileDownloadError) as exc:
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls
    assert str(exc.value) == \
        concrete_action_remote_files_instance.remote_files[0].url

  def test_invoke__file_security_failure__file_system_calls(
      self,
      concrete_action_remote_files_instance: RemoteFilesAction,
      mocked_file_security: mock.Mock,
      mocked_file_system: mock.Mock,
  ) -> None:
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_fs_calls = self.build_mocked_file_system_calls(
        concrete_action_remote_files_instance
    )[3:]

    with pytest.raises(RemoteFileDownloadError):
      concrete_action_remote_files_instance.invoke()

    assert mocked_file_system.mock_calls == expected_fs_calls
