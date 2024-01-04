"""Test fixtures for the system modules tests."""
# pylint: disable=redefined-outer-name

from contextlib import closing
from io import BytesIO
from unittest import mock

import pytest
from .. import file_security, supervisor


@pytest.fixture
def file_security_instance(
    mocked_hashlib_sha256: mock.Mock,
    mocked_open_read_binary: mock.Mock,
    mocked_file_path: str,
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
def mocked_binary_data() -> bytes:
  return b"mocked_binary_data"


@pytest.fixture
def mocked_file_handle_binary(mocked_binary_data: bytes) -> BytesIO:
  return BytesIO(mocked_binary_data)


@pytest.fixture
def mocked_file_path() -> str:
  return '/mock/file.txt'


@pytest.fixture
def mocked_hashlib_sha256() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_open_read_binary(mocked_file_handle_binary: BytesIO) -> mock.Mock:
  open_mock = mock.Mock()
  open_mock.return_value = closing(mocked_file_handle_binary)
  return open_mock


@pytest.fixture
def mocked_supervisor_server() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def supervisor_instance(
    mocked_supervisor_server: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> supervisor.SupervisorClient:
  monkeypatch.setattr(
      supervisor.__name__ + ".patched_client.Server",
      mocked_supervisor_server,
  )
  return supervisor.SupervisorClient()
