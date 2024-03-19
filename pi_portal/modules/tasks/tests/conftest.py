"""Test fixtures for the task scheduler modules tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Dict, List
from unittest import mock

import pytest
from pi_portal.modules import tasks
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.tasks.enums import RoutingLabel
from .. import flags, scheduler, service, service_client

MOCKED_CONFIG: Dict[RoutingLabel, int] = {
    RoutingLabel.PI_PORTAL_CONTROL: 2,
    RoutingLabel.ARCHIVAL: 2,
}


@pytest.fixture
def mocked_api_server() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_import_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_manifests() -> List[mock.Mock]:
  return [mock.Mock()]


@pytest.fixture
def mocked_manifest_factory(mocked_manifests: List[mock.Mock]) -> mock.Mock:
  instance = mock.Mock()
  instance.create.side_effect = mocked_manifests
  return instance


@pytest.fixture
def mocked_scheduler_logger(
    mocked_task_logger: logging.Logger,
) -> logging.Logger:
  scheduler_formatter = logging.Formatter(
      '%(levelname)s - %(task_id)s - %(task_type)s - %(queue)s - %(message)s',
      validate=False,
  )
  mocked_task_logger.handlers[0].formatter = scheduler_formatter
  return mocked_task_logger


@pytest.fixture
def mocked_worker_cron() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_worker_failed_tasks() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_worker_queue() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_service_creation_mocks(
    mocked_import_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
  monkeypatch.setattr(
      tasks.__name__ + ".import_module",
      mocked_import_module,
  )


@pytest.fixture
def mocked_task_registry_factory(mocked_task_registry: mock.Mock) -> mock.Mock:
  registry_factory = mock.Mock()
  registry_factory.return_value.create.return_value = mocked_task_registry
  return registry_factory


@pytest.fixture
def mocked_task_scheduler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_unix_stream_http_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def flags_instance() -> flags.Flags:
  return flags.Flags()


@pytest.fixture
def task_scheduler_instance_with_logger(
    mocked_task_registry_factory: mock.Mock,
    mocked_task_router: mock.Mock,
    mocked_manifest_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> scheduler.TaskScheduler:
  monkeypatch.setattr(
      scheduler.__name__ + ".QUEUE_WORKER_CONFIGURATION",
      MOCKED_CONFIG,
  )
  monkeypatch.setattr(
      scheduler.__name__ + ".RegistryFactory",
      mocked_task_registry_factory,
  )
  monkeypatch.setattr(
      scheduler.__name__ + ".TaskManifestFactory",
      mocked_manifest_factory,
  )
  monkeypatch.setattr(
      scheduler.__name__ + ".TaskRouter",
      mocked_task_router,
  )
  with mock_state.mock_state_creator():
    instance = scheduler.TaskScheduler()
  return instance


@pytest.fixture
def task_scheduler_instance(
    task_scheduler_instance_with_logger: scheduler.TaskScheduler,
    mocked_scheduler_logger: logging.Logger,
    mocked_worker_cron: mock.Mock,
    mocked_worker_failed_tasks: mock.Mock,
    mocked_worker_queue: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> scheduler.TaskScheduler:
  monkeypatch.setattr(
      scheduler.__name__ + ".CronWorker",
      mocked_worker_cron,
  )
  monkeypatch.setattr(
      scheduler.__name__ + ".FailedTaskWorker",
      mocked_worker_failed_tasks,
  )
  monkeypatch.setattr(
      scheduler.__name__ + ".QueueWorker",
      mocked_worker_queue,
  )
  monkeypatch.setattr(
      task_scheduler_instance_with_logger,
      "log",
      mocked_scheduler_logger,
  )
  return task_scheduler_instance_with_logger


@pytest.fixture
def task_scheduler_service_instance(
    mocked_task_scheduler: mock.Mock,
    mocked_api_server: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> service.TaskSchedulerService:
  monkeypatch.setattr(
      service.__name__ + ".Server",
      mocked_api_server,
  )
  monkeypatch.setattr(
      service.__name__ + ".TaskScheduler",
      mocked_task_scheduler,
  )
  return service.TaskSchedulerService()


@pytest.fixture
def task_scheduler_service_client_instance(
    mocked_unix_stream_http_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> service_client.TaskSchedulerServiceClient:
  monkeypatch.setattr(
      service_client.__name__ + ".UnixStreamHttpClient",
      mocked_unix_stream_http_client
  )
  return service_client.TaskSchedulerServiceClient()
