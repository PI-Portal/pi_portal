"""Test the RemoteFileStepBase class."""

import logging
from io import StringIO
from typing import List
from unittest import mock

import pytest
from pi_portal.modules.integrations.network import http
from pi_portal.modules.python.mock import CallType
from pi_portal.modules.system import file_security
from .. import remote_file_step, system_call_step


class TestRemoteFileStepBase:
  """Test the RemoteFileStepBase class."""

  def build_log_messages(
      self,
      remote_files: List[remote_file_step.RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "test - INFO - Download: "
                      f"'{remote_file.url}' -> '{remote_file.target}' ..."
                  ),
                  (
                      "test - INFO - Download: Successfully saved "
                      f"'{remote_file.target}' !"
                  ),
                  (
                      "test - INFO - Executing: 'chown "
                      f"{remote_file.user}:{remote_file.user} "
                      f"{remote_file.target}' ..."
                  ),
                  (
                      "test - INFO - Executing: 'chmod "
                      f"{remote_file.permissions} "
                      f"{remote_file.target}' ..."
                  ),
              ]
          ) + "\n"
      )
    return expected_logs

  def build_failed_get_log_messages(
      self,
      remote_files: List[remote_file_step.RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "test - INFO - Download: "
                      f"'{remote_file.url}' -> '{remote_file.target}' ..."
                  ),
                  (
                      "test - ERROR - Download: Unable to retrieve remote file "
                      f"from '{remote_file.url}' !"
                  )
              ]
          ) + "\n"
      )
    return expected_logs

  def build_failed_hash_log_messages(
      self,
      remote_files: List[remote_file_step.RemoteFile],
  ) -> str:
    expected_logs = "\n".join(
        [
            (
                "test - INFO - Download: "
                f"'{remote_files[0].url}' -> '{remote_files[0].target}' ..."
            ),
            (
                "test - ERROR - Download: Unexpected hash value for file "
                f"downloaded from '{remote_files[0].url}' !"
            )
        ]
    ) + "\n"
    return expected_logs

  def build_system_call_failed_log_messages(
      self,
      remote_files: List[remote_file_step.RemoteFile],
  ) -> str:
    expected_logs = ""
    for remote_file in remote_files:
      expected_logs += (
          "\n".join(
              [
                  (
                      "test - INFO - Download: "
                      f"'{remote_file.url}' -> "
                      f"'{remote_file.target}' ..."
                  ),
                  (
                      "test - INFO - Download: Successfully saved "
                      f"'{remote_file.target}' !"
                  ),
                  (
                      "test - INFO - Executing: 'chown "
                      f"{remote_file.user}:{remote_file.user} "
                      f"{remote_file.target}' ..."
                  ),
                  (
                      "test - ERROR - Command: 'chown "
                      f"{remote_file.user}:{remote_file.user} "
                      f"{remote_file.target}' failed!"
                  ),
              ]
          ) + "\n"
      )
    return expected_logs

  def build_mocked_file_security_calls(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
  ) -> List[CallType]:
    expected_file_security_calls: List[CallType] = []
    for remote_file in concrete_remote_file_step_instance.remote_files:
      expected_file_security_calls += [
          mock.call(remote_file.target),
          mock.call().sha256(remote_file.sha256),
      ]
    return expected_file_security_calls

  def build_mocked_http_client_calls(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
  ) -> List[CallType]:
    expected_http_client_calls: List[CallType] = []
    for remote_file in concrete_remote_file_step_instance.remote_files:
      expected_http_client_calls += [
          mock.call(concrete_remote_file_step_instance.log),
          mock.call().get(remote_file.url, remote_file.target),
      ]
    return expected_http_client_calls

  def build_mocked_system_calls(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
  ) -> List[CallType]:
    expected_system_calls: List[CallType] = []
    for remote_file in concrete_remote_file_step_instance.remote_files:
      expected_system_calls.append(
          mock.call(
              f"chown {remote_file.user}:{remote_file.user} "
              f"{remote_file.target}"
          )
      )
      expected_system_calls.append(
          mock.call(f"chmod {remote_file.permissions} {remote_file.target}")
      )
    return expected_system_calls

  def test__initialize__attrs(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
  ) -> None:
    assert isinstance(concrete_remote_file_step_instance.log, logging.Logger)

  def test__initialize__remote_files(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
  ) -> None:
    assert len(concrete_remote_file_step_instance.remote_files) == 2

    file1 = concrete_remote_file_step_instance.remote_files[0]
    assert isinstance(file1, remote_file_step.RemoteFile)
    assert file1.sha256 == "expected_sha256_1"
    assert file1.target == "/path/target1.txt"
    assert file1.url == "https://remote.com/source1.txt"
    assert file1.permissions == "644"
    assert file1.user == "root"

    file2 = concrete_remote_file_step_instance.remote_files[1]
    assert isinstance(file2, remote_file_step.RemoteFile)
    assert file2.sha256 == "expected_sha256_2"
    assert file2.target == "/path/target2.sh"
    assert file2.url == "https://remote.com/source2.sh"
    assert file2.permissions == "755"
    assert file2.user == "test_user"

  def test__download__logs__success(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_log_messages = \
        self.build_log_messages(
          concrete_remote_file_step_instance.remote_files
        )

    concrete_remote_file_step_instance.download()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__download__logs__download_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_http_client: mock.Mock,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_log_messages = self.build_failed_get_log_messages(
        concrete_remote_file_step_instance.remote_files[0:1]
    )
    expected_log_messages += self.build_log_messages(
        concrete_remote_file_step_instance.remote_files[1:]
    )

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__download__system_call_failure__logging(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0, 0, 0]
    expected_log_messages = \
        self.build_system_call_failed_log_messages(
          concrete_remote_file_step_instance.remote_files[0:1]
        )
    expected_log_messages += \
        self.build_log_messages(
          concrete_remote_file_step_instance.remote_files[1:]
        )

    with pytest.raises(system_call_step.SystemCallError):
      concrete_remote_file_step_instance.download()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__download__logs__validation_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_log_messages = \
        self.build_failed_hash_log_messages(
          concrete_remote_file_step_instance.remote_files[0:1]
        )
    expected_log_messages += \
        self.build_log_messages(
          concrete_remote_file_step_instance.remote_files[1:]
        )

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_stream.getvalue() == expected_log_messages

  def test__download__file_security__success(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_remote_file_step_instance
        )

    concrete_remote_file_step_instance.download()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls

  def test__download__file_security__download_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_remote_file_step_instance
        )[2:]

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls

  def test__download__file_security__system_call_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0, 0, 0]
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_remote_file_step_instance
        )

    with pytest.raises(system_call_step.SystemCallError):
      concrete_remote_file_step_instance.download()

    assert mocked_file_security.mock_calls == \
           expected_file_security_calls

  def test__download__file_security__validation_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_file_security_calls = \
        self.build_mocked_file_security_calls(
          concrete_remote_file_step_instance
        )

    with pytest.raises(remote_file_step.RemoteFileDownloadError) as exc:
      concrete_remote_file_step_instance.download()

    assert mocked_file_security.mock_calls == \
        expected_file_security_calls
    assert str(exc.value) == \
        concrete_remote_file_step_instance.remote_files[0].url

  def test__download__http_client__success(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_remote_file_step_instance
        )

    concrete_remote_file_step_instance.download()

    assert mocked_http_client.mock_calls == \
           expected_http_client_calls

  def test__download__http_client__download_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_remote_file_step_instance
        )

    with pytest.raises(remote_file_step.RemoteFileDownloadError) as exc:
      concrete_remote_file_step_instance.download()

    assert mocked_http_client.mock_calls == expected_http_client_calls
    assert str(exc.value) == \
        concrete_remote_file_step_instance.remote_files[0].url

  def test__download__http_client__system_call_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [127, 0, 0, 0]
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_remote_file_step_instance
        )

    with pytest.raises(system_call_step.SystemCallError):
      concrete_remote_file_step_instance.download()

    assert mocked_http_client.mock_calls == expected_http_client_calls

  def test__download__http_client__validation_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_http_client_calls = \
        self.build_mocked_http_client_calls(
          concrete_remote_file_step_instance
        )

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_http_client.mock_calls == expected_http_client_calls

  def test__download__system_calls__success(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    expected_system_calls = self.build_mocked_system_calls(
        concrete_remote_file_step_instance
    )

    concrete_remote_file_step_instance.download()

    assert mocked_system.mock_calls == expected_system_calls

  def test__download__system_calls__download_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_http_client: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_http_client.return_value.get.side_effect = \
        [http.HttpClientError, None]
    expected_system_calls = self.build_mocked_system_calls(
        concrete_remote_file_step_instance
    )[2:]

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_system.mock_calls == \
        expected_system_calls

  def test__download__system_calls__system_call_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.side_effect = [0, 127, 0, 0]
    expected_system_calls = self.build_mocked_system_calls(
        concrete_remote_file_step_instance
    )

    with pytest.raises(system_call_step.SystemCallError) as exc:
      concrete_remote_file_step_instance.download()

    assert mocked_system.mock_calls == expected_system_calls
    assert str(exc.value) == (
        "Command: 'chmod "
        f"{concrete_remote_file_step_instance.remote_files[0].permissions} "
        f"{concrete_remote_file_step_instance.remote_files[0].target}' failed!"
    )

  def test__download__system_calls__validation_failure(
      self,
      concrete_remote_file_step_instance: remote_file_step.RemoteFileStepBase,
      mocked_file_security: mock.Mock,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0
    mocked_file_security.return_value.sha256.side_effect = \
        [file_security.FileSecurityViolation, None]
    expected_system_calls = self.build_mocked_system_calls(
        concrete_remote_file_step_instance
    )[2:]

    with pytest.raises(remote_file_step.RemoteFileDownloadError):
      concrete_remote_file_step_instance.download()

    assert mocked_system.mock_calls == expected_system_calls
