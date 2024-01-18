"""Test fixtures for the cron job modules."""
# pylint: disable=redefined-outer-name

import logging
from collections import OrderedDict
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable, Dict, List, NamedTuple, Optional, Type
from unittest import mock

import pytest
from pi_portal.modules.tasks.conftest import Interrupt
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.workers import cron_worker, queue_worker

TypeQueueWorkerMocksCreator = Callable[[TaskType], "ScenarioMocks"]


@dataclass
class MockTaskArgs(task_args_base.TaskArgsBase):
  path: str


class RetryScenario(NamedTuple):
  retry_on_error: bool
  task_type: TaskType
  task_args: "task_args_base.TaskArgsBase"
  ok: Optional[bool]


class ScenarioMocks(NamedTuple):
  instance: "queue_worker.QueueWorker"
  mocked_processor: "mock.Mock"
  task: "Type[task_base.TypeGenericTask]"
  args: "Type[task_args_base.TaskArgsBase]"


class TaskScenario(NamedTuple):
  task_type: TaskType
  task_args: "task_args_base.TaskArgsBase"
  ok: Optional[bool]


@pytest.fixture
def create_queue_worker_scenario_mocks(
    queue_worker_instance: queue_worker.QueueWorker,
) -> TypeQueueWorkerMocksCreator:

  def creator(task_type: TaskType) -> ScenarioMocks:
    task_class = mock.Mock()
    task_class.type = task_type
    task_class.return_value.type = task_type
    task_class.return_value.on_failure = []
    task_class.return_value.on_success = []

    mocked_processor = mock.MagicMock()
    mocked_processor.type = task_type
    mocked_processor.return_value.type = task_type

    registered_task = queue_worker_instance.registry.tasks[task_type]
    queue_worker_instance.registry.processors[task_type] = mocked_processor

    setattr(registered_task, "TaskClass", task_class)

    return ScenarioMocks(
        instance=queue_worker_instance,
        mocked_processor=mocked_processor,
        task=registered_task.TaskClass,
        args=registered_task.ArgClass,
    )

  return creator


@pytest.fixture
def mocked_sleep() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def cron_worker_instance(
    mocked_task_router: mock.Mock,
    mocked_sleep: mock.Mock,
    mocked_worker_logger: logging.Logger,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> cron_worker.CronWorker:
  monkeypatch.setattr(
      cron_worker.__name__ + ".time.sleep",
      mocked_sleep,
  )
  return cron_worker.CronWorker(
      mocked_worker_logger,
      mocked_task_router,
      mocked_task_registry,
  )


@pytest.fixture
def cron_worker_instance_single_run(
    cron_worker_instance: cron_worker.CronWorker,
    mocked_sleep: mock.Mock,
) -> cron_worker.CronWorker:
  mocked_sleep.side_effect = [None, Interrupt]
  return cron_worker_instance


@pytest.fixture
def cron_worker_instance_two_runs(
    cron_worker_instance: cron_worker.CronWorker,
    mocked_sleep: mock.Mock,
) -> cron_worker.CronWorker:
  mocked_sleep.side_effect = [None, None, Interrupt]
  return cron_worker_instance


@pytest.fixture
def cron_worker_running(
    cron_worker_instance: cron_worker.CronWorker,
    mocked_task_registry_cron_jobs: List[mock.Mock],
    mocked_sleep: mock.Mock,
) -> "Future[None]":
  minimum_iterations = 10
  cron_worker_instance.jobs = mocked_task_registry_cron_jobs

  executor = ThreadPoolExecutor()
  future = executor.submit(cron_worker_instance.start)
  executor.shutdown(wait=False)

  while True:
    if mocked_sleep.call_count > minimum_iterations:  # pragma: no cover
      return future


@pytest.fixture
def queue_worker_instance(
    mocked_worker_logger: logging.Logger,
    mocked_queue: mock.Mock,
    mocked_sleep: mock.Mock,
    mocked_task_registry: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> queue_worker.QueueWorker:
  monkeypatch.setattr(
      cron_worker.__name__ + ".time.sleep",
      mocked_sleep,
  )
  return queue_worker.QueueWorker(
      mocked_worker_logger,
      TaskPriority.STANDARD,
      mocked_queue,
      mocked_task_registry,
  )


@pytest.fixture
def queue_worker_processing_sequence(
    queue_worker_instance: queue_worker.QueueWorker,
    monkeypatch: pytest.MonkeyPatch,
) -> mock.Mock:
  sequence_mock = mock.Mock()

  method_list: Dict[str, str] = OrderedDict(
      {
          "processing": "_do_task_processing",
          "ack": "_do_task_ack",
          "success": "_do_task_success",
          "failure": "_do_task_failure",
      }
  )

  for mock_name, method_name in method_list.items():
    new_mock = mock.Mock()
    new_mock.configure_mock(name=mock_name)
    monkeypatch.setattr(
        queue_worker_instance,
        method_name,
        new_mock,
    )
    sequence_mock.attach_mock(new_mock, mock_name)

  return sequence_mock


@pytest.fixture
def queue_worker_running(
    queue_worker_instance: queue_worker.QueueWorker,
    mocked_queue: mock.Mock,
) -> "Future[None]":
  minimum_iterations = 10
  mocked_queue.get.return_value.type = TaskType.NON_SCHEDULED

  executor = ThreadPoolExecutor()
  future = executor.submit(queue_worker_instance.start)
  executor.shutdown(wait=False)

  while True:
    if mocked_queue.get.call_count > minimum_iterations:  # pragma: no cover
      return future
