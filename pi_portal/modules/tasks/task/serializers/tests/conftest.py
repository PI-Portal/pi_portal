"""Test fixtures for the task scheduler api module tests."""
# pylint: disable=redefined-outer-name,unused-import

from typing import Any, Dict, List, NamedTuple

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from pi_portal.modules.tasks.task.bases.tests.conftest import (
    concrete_task_base_class,
    concrete_task_base_instance,
)
from typing_extensions import NotRequired, TypedDict


class TypedTaskParameters(TypedDict):
  type: str
  args: Dict[str, Any]
  priority: str
  retry_on_error: NotRequired[bool]
  on_failure: NotRequired[List["TypedTaskParameters"]]
  on_success: NotRequired[List["TypedTaskParameters"]]


class ClonedTasksScenario(NamedTuple):
  task1: TaskBase[MockGenericTaskArgs, str]
  task2: TaskBase[MockGenericTaskArgs, str]


@pytest.fixture(name="cloned_tasks")
def cloned_concrete_task_base_instances(
    mocked_generic_task_args: MockGenericTaskArgs,
) -> ClonedTasksScenario:

  class Task1(TaskBase[MockGenericTaskArgs, str]):
    task = TaskType.NON_SCHEDULED

  class Task2(TaskBase[MockGenericTaskArgs, str]):
    task = TaskType.QUEUE_MAINTENANCE

  task_1 = Task1(args=mocked_generic_task_args)
  task_2 = Task2(args=mocked_generic_task_args)

  return ClonedTasksScenario(
      task1=task_1,
      task2=task_2,
  )
