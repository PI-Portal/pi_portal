"""Test fixtures for the handlers modules."""
# pylint: disable=redefined-outer-name

import logging
import logging.handlers
from io import StringIO
from unittest import mock

import pytest
from .. import rotation_archived, rotation_unarchived


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
def mocked_task_scheduler_service_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def archived_rotating_file_handler_instance(
    mocked_logger_file_name: str,
    mocked_os_path_exists: mock.Mock,
    mocked_should_rotate: mock.Mock,
    mocked_task_scheduler_service_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> rotation_archived.RotatingFileHandlerArchived:
  monkeypatch.setattr(
      logging.handlers.__name__ + ".os.path.exists",
      mocked_os_path_exists,
  )
  monkeypatch.setattr(
      logging.handlers.__name__ + ".RotatingFileHandler.shouldRollover",
      mocked_should_rotate,
  )
  monkeypatch.setattr(
      rotation_archived.__name__ + ".TaskSchedulerServiceClient",
      mocked_task_scheduler_service_client,
  )
  handler = rotation_archived.RotatingFileHandlerArchived(
      mocked_logger_file_name
  )
  return handler


@pytest.fixture
def archived_logger_instance(
    archived_rotating_file_handler_instance: rotation_archived.
    RotatingFileHandlerArchived,
    mocked_logger_name: str,
    mocked_open: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> logging.Logger:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open,
  )
  log = logging.getLogger(mocked_logger_name)
  handler = archived_rotating_file_handler_instance
  handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
  log.handlers = [handler]
  log.setLevel(logging.DEBUG)
  return log


@pytest.fixture
def unarchived_rotating_file_handler_instance(
    mocked_logger_file_name: str,
) -> rotation_unarchived.RotatingFileHandlerUnarchived:
  return rotation_unarchived.RotatingFileHandlerUnarchived(
      mocked_logger_file_name
  )
