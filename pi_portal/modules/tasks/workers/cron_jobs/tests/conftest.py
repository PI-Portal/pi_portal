"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from copy import deepcopy
from io import StringIO
from unittest import mock

import pytest
from .. import (
    archive_logs,
    archive_videos,
    dead_man_switch,
    queue_maintenance,
    queue_metrics,
)


@pytest.fixture
def mocked_isolated_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_isolated_worker_logger(
    mocked_isolated_stream: StringIO,
    mocked_task_logger: logging.Logger,
) -> logging.Logger:
  cloned_logger: logging.Logger = deepcopy(mocked_task_logger)
  setattr(
      cloned_logger.handlers[0],
      "stream",
      mocked_isolated_stream,
  )
  return cloned_logger


@pytest.fixture
def archive_logs_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> archive_logs.CronJob:
  return archive_logs.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


@pytest.fixture
def archive_videos_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> archive_videos.CronJob:
  return archive_videos.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


@pytest.fixture
def dead_man_switch_cron_job_instance(
    mocked_isolated_worker_logger: logging.Logger,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> dead_man_switch.CronJob:
  instance = dead_man_switch.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
  setattr(
      instance.isolated_logger,
      "log",
      mocked_isolated_worker_logger,
  )
  return instance


@pytest.fixture
def dead_man_switch_logger_instance(
    mocked_isolated_worker_logger: logging.Logger,
) -> dead_man_switch.DeadManSwitchLogger:
  instance = dead_man_switch.DeadManSwitchLogger()
  setattr(
      instance,
      "log",
      mocked_isolated_worker_logger,
  )
  return instance


@pytest.fixture
def queue_maintenance_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> queue_maintenance.CronJob:
  return queue_maintenance.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


@pytest.fixture
def queue_metrics_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> queue_metrics.CronJob:
  metrics_formatter = logging.Formatter(
      (
          '%(levelname)s - %(task)s - %(cron)s - %(queue)s - '
          '%(metrics)s - %(message)s'
      ),
      validate=False,
  )
  mocked_worker_logger.handlers[0].formatter = metrics_formatter
  return queue_metrics.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
