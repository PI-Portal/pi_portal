"""Shared test fixtures for the cron modules tests."""
# pylint: disable=redefined-outer-name

import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal.modules.tasks.conftest import TaskLoggingFilter
from pi_portal.modules.tasks.enums import TaskManifests


@pytest.fixture
def mocked_failed_task_manifest() -> mock.Mock:
  instance = mock.Mock()
  instance.contents = []
  return instance


@pytest.fixture
def mocked_metrics_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_metrics_logger(mocked_metrics_stream: StringIO,) -> logging.Logger:
  logger = logging.getLogger("test_metrics")
  handler = logging.StreamHandler(stream=mocked_metrics_stream)
  handler.setFormatter(
      logging.Formatter(
          (
              '%(levelname)s - %(task_id)s - %(task_type)s - %(cron)s - '
              '%(queue)s - %(queue_metrics)s - '
              '%(manifest)s - %(manifest_metrics)s - '
              '%(system_metrics)s - '
              '%(message)s'
          ),
          validate=False,
      )
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  logger.filters = [TaskLoggingFilter()]
  return logger


@pytest.fixture
def mocked_task_scheduler(
    mocked_failed_task_manifest: mock.Mock,
    mocked_task_registry: mock.Mock,
    mocked_task_router: mock.Mock,
    mocked_worker_logger: logging.Logger,
) -> mock.Mock:
  instance = mock.Mock()
  instance.registry = mocked_task_registry
  instance.router = mocked_task_router()
  instance.log = mocked_worker_logger
  instance.manifests = {TaskManifests.FAILED_TASKS: mocked_failed_task_manifest}
  return instance


@pytest.fixture
def mocked_worker_logger(mocked_task_logger: logging.Logger) -> logging.Logger:
  worker_formatter = logging.Formatter(
      '%(levelname)s - %(task_id)s - %(task_type)s - '
      '%(cron)s - %(queue)s - %(message)s',
      validate=False,
  )
  mocked_task_logger.handlers[0].formatter = worker_formatter
  return mocked_task_logger
