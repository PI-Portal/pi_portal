"""Test fixtures for the system modules tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from contextlib import closing
from io import BytesIO
from unittest import mock

import pytest
from .. import (
    file_security,
    file_system,
    supervisor,
    supervisor_config,
    supervisor_process,
)


@pytest.fixture
def file_security_instance(
    mocked_file_path: str,
    mocked_hashlib_sha256: mock.Mock,
    mocked_open_read_binary: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> file_security.FileSecurity:
  monkeypatch.setattr(
      file_security.__name__ + ".sha256",
      mocked_hashlib_sha256,
  )
  monkeypatch.setattr(
      "builtins.open",
      mocked_open_read_binary,
  )
  return file_security.FileSecurity(mocked_file_path)


@pytest.fixture
def file_system_instance(
    mocked_file_path: str,
    mocked_os: mock.Mock,
    mocked_shutil: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> file_system.FileSystem:
  monkeypatch.setattr(
      file_system.__name__ + ".os",
      mocked_os,
  )
  monkeypatch.setattr(
      file_system.__name__ + ".shutil",
      mocked_shutil,
  )
  return file_system.FileSystem(mocked_file_path)


@pytest.fixture
def mocked_binary_data() -> bytes:
  return b"mocked_binary_data"


@pytest.fixture
def mocked_file_handle_binary(mocked_binary_data: bytes) -> BytesIO:
  return BytesIO(mocked_binary_data)


@pytest.fixture
def mocked_file_path() -> str:
  return '/mock/file.txt'


@pytest.fixture
def mocked_process() -> supervisor_config.ProcessList:
  return supervisor_config.ProcessList.BOT


@pytest.fixture
def mocked_hashlib_sha256() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_open_read_binary(mocked_file_handle_binary: BytesIO) -> mock.Mock:
  open_mock = mock.Mock()
  open_mock.return_value = closing(mocked_file_handle_binary)
  return open_mock


@pytest.fixture
def mocked_os() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_supervisor_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_supervisor_server() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def supervisor_client_instance(
    mocked_supervisor_server: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> supervisor.SupervisorClient:
  monkeypatch.setattr(
      supervisor.__name__ + ".patched_client.Server",
      mocked_supervisor_server,
  )
  return supervisor.SupervisorClient()


@pytest.fixture
def supervisor_process_instance(
    mocked_process: supervisor_config.ProcessList,
    mocked_supervisor_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> supervisor_process.SupervisorProcess:
  monkeypatch.setattr(
      supervisor_process.__name__ + ".supervisor.SupervisorClient",
      mocked_supervisor_client,
  )
  return supervisor_process.SupervisorProcess(mocked_process)
