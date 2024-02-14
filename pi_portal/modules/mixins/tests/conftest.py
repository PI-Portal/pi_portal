"""Test fixtures for the mixins modules tests."""
# pylint: disable=redefined-outer-name

from contextlib import closing
from io import BytesIO, StringIO
from unittest import mock

import pytest
from .. import (
    read_json_file,
    read_log_file,
    write_archived_log_file,
    write_unarchived_log_file,
)


@pytest.fixture
def mocked_file_handle_binary() -> BytesIO:
  return BytesIO()


@pytest.fixture
def mocked_file_handle_string() -> StringIO:
  return StringIO()


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


class ArchivedLoggingWriter(write_archived_log_file.ArchivedLogFileWriter):
  """A test class using the ArchivedLogFileWriter mixin."""

  logger_name = "test_archived_logger"
  log_file_path = "/var/run/some.log"


class UnarchivedLoggingWriter(
    write_unarchived_log_file.UnarchivedLogFileWriter
):
  """A test class using the UnarchivedLogFileWriter mixin."""

  logger_name = "test_unarchived_logger"
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
def log_file_archived_writer_instance(
) -> write_archived_log_file.ArchivedLogFileWriter:
  return ArchivedLoggingWriter()


@pytest.fixture
def log_file_unarchived_writer_instance(
) -> write_unarchived_log_file.UnarchivedLogFileWriter:
  return UnarchivedLoggingWriter()
