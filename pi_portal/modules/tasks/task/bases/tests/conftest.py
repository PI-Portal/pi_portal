"""Test fixtures for the task modules tests."""
# pylint: disable=redefined-outer-name

from typing import NamedTuple, Type

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.task.bases.task_base import TaskBase


class ClonedTasksScenario(NamedTuple):
  task1: TaskBase[MockGenericTaskArgs, str]
  task2: TaskBase[MockGenericTaskArgs, str]


@pytest.fixture
def concrete_task_base_class() -> Type[TaskBase[MockGenericTaskArgs, str]]:

  class ConcreteTask(TaskBase[MockGenericTaskArgs, str]):
    type = TaskType.BASE

  return ConcreteTask


@pytest.fixture
def concrete_task_base_instance(
    concrete_task_base_class: Type[TaskBase[MockGenericTaskArgs, str]],
    mocked_generic_task_args: MockGenericTaskArgs,
) -> TaskBase[MockGenericTaskArgs, str]:
  return concrete_task_base_class(mocked_generic_task_args)
