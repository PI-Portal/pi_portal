"""Test fixtures for the processor base classes."""
# pylint: disable=redefined-outer-name

import logging
from dataclasses import asdict
from typing import Callable, List, Type
from unittest import mock

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.mixins import archival_client
from pi_portal.modules.tasks.task import archive_videos
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from .. import processor_archival
from ..processor_archival import ArchivalTaskProcessorBaseClass
from ..processor_base import TaskProcessorBase

TypeConcreteProcessor = TaskProcessorBase[
    MockGenericTaskArgs,
    int,
]


@pytest.fixture
def mocked_archival_client_class() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_archival_task(
    mocked_base_task: mock.Mock,
    mocked_archival_task_args: archive_videos.Args,
    mocked_task_type: TaskType,
) -> mock.Mock:
  mocked_base_task.args = mocked_archival_task_args
  mocked_base_task.type = mocked_task_type
  return mocked_base_task


@pytest.fixture
def mocked_archival_task_args() -> archive_videos.Args:
  return archive_videos.Args(partition_name="mock_partition",)


@pytest.fixture
def mocked_mutex() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_os_remove() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_task(
    mocked_base_task: mock.Mock,
    mocked_generic_task_args: MockGenericTaskArgs,
    mocked_task_type: TaskType,
) -> mock.Mock:
  mocked_base_task.args = mocked_generic_task_args
  mocked_base_task.type = mocked_task_type
  return mocked_base_task


@pytest.fixture
def mocked_task_timing_logger(
    mocked_task_logger: logging.Logger
) -> logging.Logger:
  mocked_task_logger.handlers[0].setFormatter(
      logging.Formatter(
          '%(levelname)s - %(task)s - %(message)s - %(processing_time)s - '
          '%(scheduled_time)s - %(total_time)s'
      )
  )
  return mocked_task_logger


@pytest.fixture
def mocked_file_list() -> List[str]:
  return ["/1/file1", "/2/file2", "/3/file3"]


@pytest.fixture
def mocked_task_type() -> TaskType:
  return TaskType.NON_SCHEDULED


@pytest.fixture
def mocked_task_processor_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_archival_processor_mocks(
    mocked_archival_client_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        archival_client.__name__ + ".ArchivalClientMixin.archival_client_class",
        mocked_archival_client_class,
    )

  return setup


@pytest.fixture
def concrete_archival_task_processor_base_class(
    mocked_mutex: mock.MagicMock,
) -> Type[ArchivalTaskProcessorBaseClass]:

  class ConcreteArchivalProcessor(ArchivalTaskProcessorBaseClass):
    mutex = mocked_mutex
    type = TaskType.BASE

  return ConcreteArchivalProcessor


@pytest.fixture(name="archival_processor_instance")
# pylint: disable=invalid-name
def concrete_archival_task_processor_base_instance(
    concrete_archival_task_processor_base_class: Type[
        ArchivalTaskProcessorBaseClass,
    ],
    mocked_os_remove: mock.Mock,
    mocked_task_logger: logging.Logger,
    setup_archival_processor_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> ArchivalTaskProcessorBaseClass:
  monkeypatch.setattr(
      processor_archival.__name__ + ".os.remove",
      mocked_os_remove,
  )
  setup_archival_processor_mocks()
  return concrete_archival_task_processor_base_class(mocked_task_logger)


@pytest.fixture(name="archival_processor_instance_with_files")
# pylint: disable=invalid-name
def concrete_archival_task_processor_base_with_unlocked_mutex_and_files(
    archival_processor_instance: ArchivalTaskProcessorBaseClass,
    mocked_file_list: List[str],
    mocked_mutex: mock.Mock,
) -> ArchivalTaskProcessorBaseClass:
  mocked_mutex.locked.return_value = False
  archival_processor_instance.disk_queue_class = \
      mock.Mock(return_value=mocked_file_list)
  return archival_processor_instance


@pytest.fixture
def concrete_task_processor_base_class(
    mocked_task_processor_implementation: mock.Mock,
) -> Type[TypeConcreteProcessor]:

  class ConcreteProcessor(TypeConcreteProcessor):
    type = TaskType.BASE

    def _process(self, task: TaskBase[MockGenericTaskArgs, int]) -> int:
      mocked_task_processor_implementation(task)
      return sum(asdict(task.args).values())

  return ConcreteProcessor


@pytest.fixture
def concrete_task_processor_base_instance(
    concrete_task_processor_base_class: Type[TypeConcreteProcessor],
    mocked_task_logger: logging.Logger,
) -> TypeConcreteProcessor:
  return concrete_task_processor_base_class(mocked_task_logger)


@pytest.fixture
def concrete_task_processor_base_instance_with_timings(
    concrete_task_processor_base_class: Type[TypeConcreteProcessor],
    mocked_task_timing_logger: logging.Logger,
) -> TypeConcreteProcessor:
  return concrete_task_processor_base_class(mocked_task_timing_logger)
