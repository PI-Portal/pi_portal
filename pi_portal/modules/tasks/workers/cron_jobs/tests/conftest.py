"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from typing import Callable, NamedTuple
from unittest import mock

import pytest
from .. import (
    archive_logs,
    archive_videos,
    manifest_metrics,
    queue_maintenance,
    queue_metrics,
    system_metrics,
)

TypeSystemMetricsScenarioCreator = Callable[
    ["SystemMetricsScenario"],
    "SystemMetricsScenarioMocks",
]


class SystemMetricsScenario(NamedTuple):
  disk_usage_free_mb: float
  cpu_used_percent: float
  virtual_memory_used_percent: float


class SystemMetricsScenarioMocks(NamedTuple):
  system_metrics_cron_job_instance: system_metrics.CronJob
  mocked_psutil_module: mock.Mock
  mocked_shutil_module: mock.Mock
  mocked_task_scheduler: mock.Mock


@pytest.fixture
def create_system_metrics_scenario(
    system_metrics_cron_job_instance: system_metrics.CronJob,
    mocked_psutil_module: mock.Mock,
    mocked_shutil_module: mock.Mock,
    mocked_task_scheduler: mock.Mock,
) -> "TypeSystemMetricsScenarioCreator":

  def setup(scenario: "SystemMetricsScenario") -> "SystemMetricsScenarioMocks":
    mocked_shutil_module.disk_usage.return_value.free = (
        scenario.disk_usage_free_mb * 1000000
    )
    mocked_psutil_module.cpu_percent.return_value = scenario.cpu_used_percent
    mocked_psutil_module.virtual_memory.return_value.percent = (
        scenario.virtual_memory_used_percent
    )

    return SystemMetricsScenarioMocks(
        system_metrics_cron_job_instance=system_metrics_cron_job_instance,
        mocked_psutil_module=mocked_psutil_module,
        mocked_shutil_module=mocked_shutil_module,
        mocked_task_scheduler=mocked_task_scheduler
    )

  return setup


@pytest.fixture()
def mocked_psutil_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil_module() -> mock.Mock:
  return mock.Mock()


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
def manifest_metrics_cron_job_instance(
    mocked_metrics_logger: logging.Logger,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> manifest_metrics.CronJob:
  instance = manifest_metrics.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
  instance.metrics_logger.log = mocked_metrics_logger
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
    mocked_metrics_logger: logging.Logger,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> queue_metrics.CronJob:
  instance = queue_metrics.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
  instance.metrics_logger.log = mocked_metrics_logger
  return instance


@pytest.fixture
def system_metrics_cron_job_instance(
    mocked_metrics_logger: logging.Logger,
    mocked_worker_logger: logging.Logger,
    mocked_psutil_module: mock.Mock,
    mocked_shutil_module: mock.Mock,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> system_metrics.CronJob:
  monkeypatch.setattr(
      system_metrics.__name__ + ".psutil",
      mocked_psutil_module,
  )
  monkeypatch.setattr(
      system_metrics.__name__ + ".shutil",
      mocked_shutil_module,
  )
  instance = system_metrics.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
  instance.metrics_logger.log = mocked_metrics_logger
  return instance
