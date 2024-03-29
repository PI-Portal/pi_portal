"""Shared test fixtures for the cron modules tests."""
# pylint: disable=redefined-outer-name

import logging
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskManifests


@pytest.fixture
def mocked_failed_task_manifest() -> mock.Mock:
  instance = mock.Mock()
  instance.contents = []
  return instance


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
      '%(levelname)s - %(task)s - %(cron)s - %(queue)s - %(message)s',
      validate=False,
  )
  mocked_task_logger.handlers[0].formatter = worker_formatter
  return mocked_task_logger
