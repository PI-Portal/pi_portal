"""Test fixtures for the mixins modules tests."""
# pylint: disable=redefined-outer-name

from contextlib import closing
from io import BytesIO, StringIO
from unittest import mock

import pytest
from .. import read_json_file, read_log_file, write_log_file


@pytest.fixture
def mocked_file_handle_binary() -> BytesIO:
  return BytesIO()


@pytest.fixture
def mocked_file_handle_string() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_get_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_json_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_open_read_binary(mocked_file_handle_binary: BytesIO) -> mock.Mock:
  open_mock = mock.Mock()
  open_mock.return_value = closing(mocked_file_handle_binary)
  return open_mock


@pytest.fixture
def mocked_open_read_string(mocked_file_handle_string: StringIO) -> mock.Mock:
  open_mock = mock.Mock()
  open_mock.return_value = closing(mocked_file_handle_string)
  return open_mock


class LoggingReader(read_log_file.LogFileReader):
  """A test class using the LogFileReader mixin."""

  logger_name = "test_logger"
  log_file_path = "/var/run/some.log"


class LoggingWriter(write_log_file.LogFileWriter):
  """A test class using the LogFileWriter mixin."""

  logger_name = "test_logger"
  log_file_path = "/var/run/some.log"


@pytest.fixture
def json_file_reader_instance(
    monkeypatch: pytest.MonkeyPatch, mocked_open_read_string: StringIO
) -> read_json_file.JSONFileReader:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open_read_string,
  )
  return read_json_file.JSONFileReader()


@pytest.fixture
def log_file_reader_instance(
    monkeypatch: pytest.MonkeyPatch,
    mocked_open_read_binary: mock.Mock,
) -> read_log_file.LogFileReader:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open_read_binary,
  )
  return LoggingReader()


@pytest.fixture
def log_file_writer_instance(
    mocked_get_logger: mock.Mock,
    mocked_json_logger: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> write_log_file.LogFileWriter:
  monkeypatch.setattr(
      write_log_file.__name__ + ".getLogger",
      mocked_get_logger,
  )
  monkeypatch.setattr(
      write_log_file.__name__ + ".JsonLoggerConfiguration",
      mocked_json_logger,
  )
  return LoggingWriter()
