"""Test fixtures for the processor base classes."""
# pylint: disable=redefined-outer-name

import logging
from dataclasses import asdict
from typing import List, Type
from unittest import mock

import pytest
from pi_portal.modules.configuration import state
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskType
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
    mocked_archival_task_args: archive_videos.Args,
    mocked_task_type: TaskType,
) -> mock.Mock:
  task = mock.Mock()
  task.args = mocked_archival_task_args
  task.type = mocked_task_type
  return task


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
    mocked_generic_task_args: MockGenericTaskArgs,
    mocked_task_type: TaskType,
) -> mock.Mock:
  task = mock.Mock()
  task.args = mocked_generic_task_args
  task.type = mocked_task_type
  return task


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
    mocked_state: state.State,
    mocked_task_logger: logging.Logger,
    monkeypatch: pytest.MonkeyPatch,
) -> ArchivalTaskProcessorBaseClass:
  state.State().user_config = mocked_state.user_config
  instance = concrete_archival_task_processor_base_class(mocked_task_logger)
  monkeypatch.setattr(
      processor_archival.__name__ + ".os.remove",
      mocked_os_remove,
  )
  return instance


@pytest.fixture(name="archival_processor_instance_with_files")
# pylint: disable=invalid-name
def concrete_archival_task_processor_base_with_unlocked_mutex_and_files(
    archival_processor_instance: ArchivalTaskProcessorBaseClass,
    mocked_archival_client_class: mock.Mock,
    mocked_file_list: List[str],
    mocked_mutex: mock.Mock,
) -> ArchivalTaskProcessorBaseClass:
  mocked_mutex.locked.return_value = False
  archival_processor_instance.archival_client_class = \
      mocked_archival_client_class
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
