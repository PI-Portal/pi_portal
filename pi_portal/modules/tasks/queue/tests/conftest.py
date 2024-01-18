"""Test fixtures for the queue implementation classes."""
# pylint: disable=redefined-outer-name

import logging
from typing import Callable, List, NamedTuple, Type, TypedDict
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskPriority
from .. import persist_queue, persist_queue_router

TypeMetricsScenarioCreator = Callable[["MetricsScenario"], None]


class TypeMockRawTask(TypedDict):
  pqid: int
  data: mock.Mock


class MetricsScenario(NamedTuple):
  files_sizes: List[float]
  size: int
  acked_count: int
  unacked_count: int


@pytest.fixture
def mocked_os_makedirs() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_path_getsize() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_scandir() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_priority_queues() -> List[mock.Mock]:
  return [mock.Mock()] * len(TaskPriority)


@pytest.fixture
def mocked_queue_implementation() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_raw_task(mocked_task: mock.Mock,) -> TypeMockRawTask:
  return TypeMockRawTask(
      pqid=99,
      data=mocked_task,
  )


@pytest.fixture
def mocked_router_queue(
    mocked_priority_queues: List[mock.Mock],
) -> List[mock.Mock]:
  return mock.Mock(side_effect=mocked_priority_queues)


@pytest.fixture
def mocked_shutil() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_task() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def persist_queue_instance_class(
    mocked_os_makedirs: mock.Mock,
    mocked_queue_implementation: mock.Mock,
    mocked_shutil: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[persist_queue.Queue]:
  monkeypatch.setattr(
      persist_queue.__name__ + ".VendorQueue",
      mocked_queue_implementation,
  )
  monkeypatch.setattr(
      persist_queue.__name__ + ".os.makedirs",
      mocked_os_makedirs,
  )
  monkeypatch.setattr(
      persist_queue.__name__ + ".shutil",
      mocked_shutil,
  )
  return persist_queue.Queue


@pytest.fixture
def persist_queue_instance_standard(
    persist_queue_instance_class: Type[persist_queue.Queue],
    mocked_queue_logger: logging.Logger,
) -> persist_queue.Queue:
  return persist_queue_instance_class(
      mocked_queue_logger,
      priority=TaskPriority.STANDARD,
  )


@pytest.fixture(name="persist_queue_instance_with_metrics_mocks")
def persist_queue_instance_standard_with_metrics_mocks(
    persist_queue_instance_standard: persist_queue.Queue,
    mocked_os_path_getsize: mock.Mock,
    mocked_os_scandir: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> persist_queue.Queue:
  monkeypatch.setattr(
      persist_queue.__name__ + ".os.path.getsize",
      mocked_os_path_getsize,
  )
  monkeypatch.setattr(
      persist_queue.__name__ + ".os.scandir",
      mocked_os_scandir,
  )
  return persist_queue_instance_standard


@pytest.fixture
def persist_queue_metrics_scenario_creator(
    mocked_os_path_getsize: mock.Mock,
    mocked_os_scandir: mock.Mock,
    mocked_queue_implementation: mock.Mock,
) -> Callable[[MetricsScenario], None]:

  def create(scenario: MetricsScenario) -> None:
    mocked_file = mock.Mock()
    mocked_file.is_file.return_value = True
    mocked_folder = mock.Mock()
    mocked_folder.is_file.return_value = False
    mocked_os_path_getsize.side_effect = scenario.files_sizes
    mocked_queue_implementation.return_value.size = \
        scenario.size
    mocked_queue_implementation.return_value.acked_count.return_value = \
        scenario.acked_count
    mocked_queue_implementation.return_value.unack_count.return_value = \
        scenario.unacked_count
    mocked_os_scandir.return_value = [mocked_file] * len(scenario.files_sizes)
    mocked_os_scandir.return_value += [mocked_folder] * 10

  return create


@pytest.fixture
def persist_queue_task_router_instance(
    mocked_router_queue: mock.Mock,
    mocked_queue_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> persist_queue_router.TaskRouter:
  monkeypatch.setattr(
      persist_queue_router.__name__ + ".Queue",
      mocked_router_queue,
  )
  return persist_queue_router.TaskRouter(mocked_queue_logger)
