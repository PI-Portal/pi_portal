"""Test the SerializedTask class."""

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from pi_portal.modules.tasks.task.bases.task_fields import TaskFields
from pi_portal.modules.tasks.task.bases.tests.conftest import (
    ClonedTasksScenario,
)
from pi_portal.modules.tasks.task.utility import compare
from ..task_serializer import SerializedTask


class TestSerializedTask:
  """Test the SerializedTask class."""

  def test_inheritance(self) -> None:
    assert issubclass(SerializedTask, TaskFields)

  @pytest.mark.parametrize(
      "test_type",
      [
          TaskType.BASE,
          TaskType.NON_SCHEDULED,
      ],
  )
  def test_serialize__correct_type_attribute(
      self,
      mocked_generic_task_args: MockGenericTaskArgs,
      test_type: TaskType,
  ) -> None:

    class SubClassedTask(TaskBase[MockGenericTaskArgs, str]):
      type = test_type

    instance = SubClassedTask(mocked_generic_task_args)

    serialized_task = SerializedTask.serialize(instance)

    assert serialized_task.type == test_type

  def test_serialize__no_completion_tasks__correct_attributes(
      self,
      concrete_task_base_instance: TaskBase[MockGenericTaskArgs, str],
  ) -> None:
    serialized_task = SerializedTask.serialize(concrete_task_base_instance)

    compare.assert_task_equals_serialized_task(
        concrete_task_base_instance,
        serialized_task,
    )

  @pytest.mark.parametrize(
      "completion_attribute",
      ["on_failure", "on_success"],
  )
  def test_serialize__vary_completion_tasks__correct_top_level_attributes(
      self,
      cloned_tasks: ClonedTasksScenario,
      concrete_task_base_instance: TaskBase[MockGenericTaskArgs, str],
      completion_attribute: str,
  ) -> None:
    setattr(
        concrete_task_base_instance,
        completion_attribute,
        [cloned_tasks.task1, cloned_tasks.task2],
    )

    serialized_task = SerializedTask.serialize(concrete_task_base_instance)

    assert len(getattr(serialized_task, completion_attribute)) == 2
    compare.assert_task_equals_serialized_task(
        concrete_task_base_instance,
        serialized_task,
    )

  @pytest.mark.parametrize(
      "completion_attribute",
      ["on_failure", "on_success"],
  )
  def test_serialize__vary_completion_tasks__correct_nested_attributes(
      self,
      cloned_tasks: ClonedTasksScenario,
      concrete_task_base_instance: TaskBase[MockGenericTaskArgs, str],
      completion_attribute: str,
  ) -> None:
    setattr(
        concrete_task_base_instance,
        completion_attribute,
        [cloned_tasks.task1, cloned_tasks.task2],
    )

    serialized_task = SerializedTask.serialize(concrete_task_base_instance)

    for index in range(0, 2):
      instance_completion_task = getattr(
          concrete_task_base_instance,
          completion_attribute,
      )[index]
      serializer_completion_task = getattr(
          serialized_task,
          completion_attribute,
      )[index]
      compare.assert_task_equals_serialized_task(
          instance_completion_task,
          serializer_completion_task,
      )
      assert instance_completion_task.type == serializer_completion_task.type
