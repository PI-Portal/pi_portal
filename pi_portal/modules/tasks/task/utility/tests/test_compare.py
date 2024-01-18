"""Test the compare utility module."""

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.task.bases.task_base import TaskBase
from pi_portal.modules.tasks.task.bases.tests.conftest import (
    ClonedTasksScenario,
)
from pi_portal.modules.tasks.task.serializers.task_serializer import (
    SerializedTask,
)
from ..compare import assert_task_equals_serialized_task


class TestAsertTaskEqualsSerializedTask:
  """Test the assert_task_equals_serialized_task function."""

  mro_slots = [
      getattr(klass, '__slots__', ()) for klass in SerializedTask.mro()
  ]

  def test_simple_case__matching__assertions_pass(
      self,
      concrete_task_base_instance: TaskBase[
          MockGenericTaskArgs,
          str,
      ],
  ) -> None:
    serialized_task_instance = SerializedTask.serialize(
        concrete_task_base_instance
    )

    assert_task_equals_serialized_task(
        concrete_task_base_instance,
        serialized_task_instance,
    )

  @pytest.mark.parametrize(
      "altered_attribute",
      [slot for slots in mro_slots for slot in slots],
  )
  def test_simple_case__vary_not_matching__assertions_fail(
      self,
      concrete_task_base_instance: TaskBase[
          MockGenericTaskArgs,
          str,
      ],
      altered_attribute: str,
  ) -> None:
    pre_alteration_serialized_task = SerializedTask.serialize(
        concrete_task_base_instance
    )
    setattr(
        concrete_task_base_instance,
        altered_attribute,
        "NON_MATCHING_ATTRIBUTE",
    )

    with pytest.raises(AssertionError):
      assert_task_equals_serialized_task(
          concrete_task_base_instance,
          pre_alteration_serialized_task,
      )

  @pytest.mark.parametrize(
      "on_completion_attribute",
      ["on_failure", "on_success"],
  )
  def test_nested_case__vary_nested_attr__assertions_pass(
      self,
      cloned_tasks: ClonedTasksScenario,
      concrete_task_base_instance: TaskBase[
          MockGenericTaskArgs,
          str,
      ],
      on_completion_attribute: str,
  ) -> None:
    setattr(
        concrete_task_base_instance,
        on_completion_attribute,
        [cloned_tasks.task1, cloned_tasks.task2],
    )
    serialized_task_instance = SerializedTask.serialize(
        concrete_task_base_instance
    )

    assert_task_equals_serialized_task(
        concrete_task_base_instance,
        serialized_task_instance,
    )

  @pytest.mark.parametrize(
      "on_completion_attribute",
      ["on_failure", "on_success"],
  )
  @pytest.mark.parametrize(
      "altered_attribute",
      [slot for slots in mro_slots for slot in slots],
  )
  def test_nested_case__vary_nested_attr__vary_non_matching__assertions_fail(
      self,
      cloned_tasks: ClonedTasksScenario,
      concrete_task_base_instance: TaskBase[
          MockGenericTaskArgs,
          str,
      ],
      on_completion_attribute: str,
      altered_attribute: str,
  ) -> None:
    setattr(
        concrete_task_base_instance,
        on_completion_attribute,
        [cloned_tasks.task1, cloned_tasks.task2],
    )
    serialized_task = SerializedTask.serialize(concrete_task_base_instance)
    setattr(
        serialized_task,
        altered_attribute,
        "NON_MATCHING_ATTRIBUTE",
    )

    with pytest.raises(AssertionError):
      assert_task_equals_serialized_task(
          concrete_task_base_instance,
          serialized_task,
      )
