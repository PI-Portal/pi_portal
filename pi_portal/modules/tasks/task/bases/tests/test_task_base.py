"""Test the TaskBase class."""

from datetime import datetime
from typing import TYPE_CHECKING, Type

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from .. import task_fields

if TYPE_CHECKING:  # pragma: no cover
  from .. import task_base


class TestTaskBase:
  """Test the TaskBase class."""

  def test_initialize__default_priority__attributes(
      self,
      concrete_task_base_instance: "task_base.TypeGenericTask",
      mocked_generic_task_args: MockGenericTaskArgs,
  ) -> None:
    assert concrete_task_base_instance.args == mocked_generic_task_args
    assert concrete_task_base_instance.completed is None
    assert isinstance(concrete_task_base_instance.created, datetime)
    assert concrete_task_base_instance.id is None
    assert concrete_task_base_instance.priority is TaskPriority.STANDARD
    assert concrete_task_base_instance.ok is None
    assert concrete_task_base_instance.on_success == []
    assert concrete_task_base_instance.on_failure == []
    assert concrete_task_base_instance.result is None
    assert concrete_task_base_instance.retry_on_error is False
    assert concrete_task_base_instance.scheduled is None
    assert concrete_task_base_instance.type == TaskType.BASE

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_initialize__vary_priority__attributes(
      self,
      concrete_task_base_class: "Type[task_base.TypeGenericTask]",
      mocked_generic_task_args: MockGenericTaskArgs,
      priority: TaskPriority,
  ) -> None:
    prioritized_task_base_instance = concrete_task_base_class(
        mocked_generic_task_args,
        priority=priority,
    )

    assert prioritized_task_base_instance.args == mocked_generic_task_args
    assert prioritized_task_base_instance.completed is None
    assert isinstance(prioritized_task_base_instance.created, datetime)
    assert prioritized_task_base_instance.id is None
    assert prioritized_task_base_instance.priority is priority
    assert prioritized_task_base_instance.ok is None
    assert prioritized_task_base_instance.on_success == []
    assert prioritized_task_base_instance.on_failure == []
    assert prioritized_task_base_instance.result is None
    assert prioritized_task_base_instance.retry_on_error is False
    assert prioritized_task_base_instance.scheduled is None
    assert prioritized_task_base_instance.type == TaskType.BASE

  @pytest.mark.parametrize("retry_on_error", [True, False])
  def test_initialize__vary_retry__attributes(
      self,
      concrete_task_base_class: "Type[task_base.TypeGenericTask]",
      mocked_generic_task_args: MockGenericTaskArgs,
      retry_on_error: bool,
  ) -> None:
    prioritized_task_base_instance = concrete_task_base_class(
        mocked_generic_task_args,
        retry_on_error=retry_on_error,
    )

    assert prioritized_task_base_instance.args == mocked_generic_task_args
    assert prioritized_task_base_instance.completed is None
    assert isinstance(prioritized_task_base_instance.created, datetime)
    assert prioritized_task_base_instance.id is None
    assert prioritized_task_base_instance.priority is TaskPriority.STANDARD
    assert prioritized_task_base_instance.ok is None
    assert prioritized_task_base_instance.on_success == []
    assert prioritized_task_base_instance.on_failure == []
    assert prioritized_task_base_instance.result is None
    assert prioritized_task_base_instance.retry_on_error is retry_on_error
    assert prioritized_task_base_instance.scheduled is None
    assert prioritized_task_base_instance.type == TaskType.BASE

  def test_initialize__inheritance(
      self,
      concrete_task_base_instance: "task_base.TypeGenericTask",
  ) -> None:
    assert isinstance(concrete_task_base_instance, task_fields.TaskFields)

  def test_str__correct_string(
      self,
      concrete_task_base_instance: "task_base.TypeGenericTask",
  ) -> None:
    concrete_task_base_instance.id = 1

    assert str(concrete_task_base_instance) == \
        f"Task(id:{concrete_task_base_instance.id}, type:" \
        f"{concrete_task_base_instance.type.value})"
