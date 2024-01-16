"""Test fixtures for the handlers modules."""
# pylint: disable=redefined-outer-name

import logging
import logging.handlers
from io import StringIO
from unittest import mock

import pytest
from .. import rotation


@pytest.fixture
def mocked_file_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_logger_file_name() -> str:
  return "/var/log/mock.log"


@pytest.fixture
def mocked_open(
    mocked_logger_stream: StringIO,
    mocked_rotated_logger_stream: StringIO,
) -> mock.Mock:
  return mock.Mock(
      side_effect=(
          mocked_logger_stream,
          mocked_rotated_logger_stream,
      )
  )


@pytest.fixture
def mocked_os_path_exists() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_rotated_logger_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_should_rotate() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def queuing_rotating_file_handler_instance(
    mocked_file_system: mock.Mock,
    mocked_logger_file_name: str,
    mocked_os_path_exists: mock.Mock,
    mocked_should_rotate: mock.Mock,
    mocked_shutil: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> rotation.RotatingFileHandlerWithEnqueue:
  monkeypatch.setattr(
      rotation.__name__ + ".file_system.FileSystem",
      mocked_file_system,
  )
  monkeypatch.setattr(
      logging.handlers.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  monkeypatch.setattr(
      logging.handlers.__name__ + ".RotatingFileHandler.shouldRollover",
      mocked_should_rotate,
  )
  monkeypatch.setattr(
      rotation.__name__ + ".shutil",
      mocked_shutil,
  )
  handler = rotation.RotatingFileHandlerWithEnqueue(mocked_logger_file_name)
  return handler


@pytest.fixture
def rotating_logger_instance(
    queuing_rotating_file_handler_instance: rotation.
    RotatingFileHandlerWithEnqueue,
    mocked_logger_name: str,
    mocked_open: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> logging.Logger:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open,
  )
  log = logging.getLogger(mocked_logger_name)
  handler = queuing_rotating_file_handler_instance
  handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
  log.handlers = [handler]
  log.setLevel(logging.DEBUG)
  return log
