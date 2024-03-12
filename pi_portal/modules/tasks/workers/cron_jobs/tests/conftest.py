"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from typing import Callable, NamedTuple
from unittest import mock

import pytest
from pi_portal.modules.system import supervisor_process
from .. import (
    archive_logs,
    archive_videos,
    disk_space,
    manifest_metrics,
    queue_maintenance,
    queue_metrics,
    system_metrics,
)

TypeDiskSpaceScenarioCreator = Callable[
    ["DiskSpaceScenario"],
    "DiskSpaceScenarioMocks",
]

TypeSystemMetricsScenarioCreator = Callable[
    ["SystemMetricsScenario"],
    "SystemMetricsScenarioMocks",
]


class DiskSpaceScenario(NamedTuple):
  low_disk_space: bool
  camera_running: bool


class DiskSpaceScenarioMocks(NamedTuple):
  disk_space_cron_job_instance: disk_space.CronJob
  mocked_shutil: mock.Mock
  mocked_supervisor_process: mock.Mock
  mocked_task_scheduler: mock.Mock
  mocked_task_scheduler_client: mock.Mock


class SystemMetricsScenario(NamedTuple):
  disk_usage_percent: float
  cpu_used_percent: float
  memory_used_percent: float


class SystemMetricsScenarioMocks(NamedTuple):
  system_metrics_cron_job_instance: system_metrics.CronJob
  mocked_system_metrics: mock.Mock
  mocked_task_scheduler: mock.Mock


@pytest.fixture
def create_disk_space_scenario(
    disk_space_cron_job_instance: disk_space.CronJob,
    mocked_shutil: mock.Mock,
    mocked_supervisor_process: mock.Mock,
    mocked_task_scheduler: mock.Mock,
    mocked_task_scheduler_client: mock.Mock,
) -> TypeDiskSpaceScenarioCreator:

  def setup(scenario: "DiskSpaceScenario") -> "DiskSpaceScenarioMocks":
    mocked_shutil.disk_usage.return_value.free = (
        (1000000 * disk_space_cron_job_instance.threshold_value)
    )
    mocked_supervisor_process.return_value.stop.side_effect = None

    if scenario.low_disk_space:
      mocked_shutil.disk_usage.return_value.free = (
          (1000000 * disk_space_cron_job_instance.threshold_value) - 1
      )
    if not scenario.camera_running:
      mocked_supervisor_process.return_value.stop.side_effect = (
          supervisor_process.SupervisorProcessException
      )

    return DiskSpaceScenarioMocks(
        disk_space_cron_job_instance=disk_space_cron_job_instance,
        mocked_shutil=mocked_shutil,
        mocked_supervisor_process=mocked_supervisor_process,
        mocked_task_scheduler=mocked_task_scheduler,
        mocked_task_scheduler_client=mocked_task_scheduler_client
    )

  return setup


@pytest.fixture
def create_system_metrics_scenario(
    system_metrics_cron_job_instance: system_metrics.CronJob,
    mocked_system_metrics: mock.Mock,
    mocked_task_scheduler: mock.Mock,
) -> "TypeSystemMetricsScenarioCreator":

  def setup(scenario: "SystemMetricsScenario") -> "SystemMetricsScenarioMocks":
    mocked_system_metrics.return_value.disk_usage_threshold.return_value = (
        scenario.disk_usage_percent
    )
    mocked_system_metrics.return_value.cpu_usage.return_value = (
        scenario.cpu_used_percent
    )
    mocked_system_metrics.return_value.memory_usage.return_value = (
        scenario.memory_used_percent
    )

    return SystemMetricsScenarioMocks(
        system_metrics_cron_job_instance=system_metrics_cron_job_instance,
        mocked_system_metrics=mocked_system_metrics,
        mocked_task_scheduler=mocked_task_scheduler
    )

  return setup


@pytest.fixture
def mocked_system_metrics() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_task_scheduler_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_supervisor_process() -> mock.Mock:
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
def disk_space_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_shutil: mock.Mock,
    mocked_supervisor_process: mock.Mock,
    mocked_task_scheduler_client: mock.Mock,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> disk_space.CronJob:
  monkeypatch.setattr(
      disk_space.__name__ + ".shutil",
      mocked_shutil,
  )
  monkeypatch.setattr(
      disk_space.__name__ + ".service_client.TaskSchedulerServiceClient",
      mocked_task_scheduler_client,
  )
  monkeypatch.setattr(
      disk_space.__name__ + ".supervisor_process.SupervisorProcess",
      mocked_supervisor_process,
  )
  return disk_space.CronJob(
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
    mocked_system_metrics: mock.Mock,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> system_metrics.CronJob:
  monkeypatch.setattr(
      system_metrics.__name__ + ".metrics.SystemMetrics",
      mocked_system_metrics,
  )
  instance = system_metrics.CronJob(
      mocked_worker_logger,
      mocked_task_registry,
  )
  instance.metrics_logger.log = mocked_metrics_logger
  return instance
