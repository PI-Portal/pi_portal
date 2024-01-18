"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from .. import (
    archive_logs,
    archive_videos,
    dead_man_switch,
    queue_maintenance,
    queue_metrics,
)


@pytest.fixture
def archive_logs_cron_job_instance(
    mocked_state: state.State,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> archive_logs.CronJob:
  state.State().user_config = mocked_state.user_config
  return archive_logs.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


@pytest.fixture
def archive_videos_cron_job_instance(
    mocked_state: state.State,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> archive_videos.CronJob:
  state.State().user_config = mocked_state.user_config
  return archive_videos.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


@pytest.fixture
def dead_man_switch_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> dead_man_switch.CronJob:
  return dead_man_switch.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )


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
