"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from copy import deepcopy
from io import StringIO
from typing import Callable, NamedTuple
from unittest import mock

import pytest
from pi_portal.modules.system import supervisor_process
from .. import (
    archive_logs,
    archive_videos,
    dead_man_switch,
    disk_space,
    manifest_metrics,
    queue_maintenance,
    queue_metrics,
)

TypeDiskSpaceScenarioCreator = Callable[
    ["DiskSpaceScenario"],
    "DiskSpaceScenarioMocks",
]


class DiskSpaceScenario(NamedTuple):
  low_disk_space: bool
  camera_running: bool


class DiskSpaceScenarioMocks(NamedTuple):
  disk_space_cron_job_instance: disk_space.CronJob
  mocked_shutil_module: mock.Mock
  mocked_supervisor_process: mock.Mock
  mocked_task_scheduler: mock.Mock
  mocked_task_scheduler_client: mock.Mock


@pytest.fixture
def create_disk_space_scenario(
    disk_space_cron_job_instance: disk_space.CronJob,
    mocked_shutil_module: mock.Mock,
    mocked_supervisor_process: mock.Mock,
    mocked_task_scheduler: mock.Mock,
    mocked_task_scheduler_client: mock.Mock,
) -> TypeDiskSpaceScenarioCreator:

  def setup(scenario: "DiskSpaceScenario") -> "DiskSpaceScenarioMocks":
    mocked_shutil_module.disk_usage.return_value.free = (
        (1000000 * disk_space_cron_job_instance.threshold_value)
    )
    mocked_supervisor_process.return_value.stop.side_effect = None

    if scenario.low_disk_space:
      mocked_shutil_module.disk_usage.return_value.free = (
          (1000000 * disk_space_cron_job_instance.threshold_value) - 1
      )
    if not scenario.camera_running:
      mocked_supervisor_process.return_value.stop.side_effect = (
          supervisor_process.SupervisorProcessException
      )

    return DiskSpaceScenarioMocks(
        disk_space_cron_job_instance=disk_space_cron_job_instance,
        mocked_shutil_module=mocked_shutil_module,
        mocked_supervisor_process=mocked_supervisor_process,
        mocked_task_scheduler=mocked_task_scheduler,
        mocked_task_scheduler_client=mocked_task_scheduler_client
    )

  return setup


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
def mocked_task_scheduler_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil_module() -> mock.Mock:
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
def disk_space_cron_job_instance(
    mocked_worker_logger: logging.Logger,
    mocked_shutil_module: mock.Mock,
    mocked_supervisor_process: mock.Mock,
    mocked_task_scheduler_client: mock.Mock,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> disk_space.CronJob:
  monkeypatch.setattr(
      disk_space.__name__ + ".shutil",
      mocked_shutil_module,
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
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
) -> manifest_metrics.CronJob:
  metrics_formatter = logging.Formatter(
      '%(levelname)s - %(task)s - %(cron)s - %(metrics)s - %(message)s',
      validate=False,
  )
  mocked_worker_logger.handlers[0].formatter = metrics_formatter
  return manifest_metrics.CronJob(
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
