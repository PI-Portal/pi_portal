"""Test the TaskBase class."""

from datetime import datetime
from typing import TYPE_CHECKING, Type

import pytest
from pi_portal.modules.tasks.conftest import MockGenericTaskArgs
from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
from .. import task_fields, task_result

if TYPE_CHECKING:  # pragma: no cover
  from .. import task_base


class TestTaskBase:
  """Test the TaskBase class."""

  def test_initialize__defaults__attributes(
      self,
      concrete_task_base_instance: "task_base.TypeGenericTask",
      mocked_generic_task_args: MockGenericTaskArgs,
  ) -> None:
    assert concrete_task_base_instance.args == mocked_generic_task_args
    assert concrete_task_base_instance.completed is None
    assert isinstance(concrete_task_base_instance.created, datetime)
    assert concrete_task_base_instance.id is None
    assert concrete_task_base_instance.ok is None
    assert concrete_task_base_instance.on_success == []
    assert concrete_task_base_instance.on_failure == []
    assert isinstance(
        concrete_task_base_instance.result, task_result.TaskResult
    )
    assert concrete_task_base_instance.result.cause is None
    assert concrete_task_base_instance.result.value is None
    assert concrete_task_base_instance.retry_after == 0
    assert concrete_task_base_instance.routing_label == (
        RoutingLabel.PI_PORTAL_CONTROL
    )
    assert concrete_task_base_instance.scheduled is None
    assert concrete_task_base_instance.type == TaskType.BASE

  @pytest.mark.parametrize("retry_after", [-1, 1])
  def test_initialize__vary_retry__attributes(
      self,
      concrete_task_base_class: "Type[task_base.TypeGenericTask]",
      mocked_generic_task_args: MockGenericTaskArgs,
      retry_after: bool,
  ) -> None:
    task_base_instance = concrete_task_base_class(
        mocked_generic_task_args,
        retry_after=retry_after,
    )

    assert task_base_instance.args == mocked_generic_task_args
    assert task_base_instance.completed is None
    assert isinstance(task_base_instance.created, datetime)
    assert task_base_instance.id is None
    assert task_base_instance.ok is None
    assert task_base_instance.on_success == []
    assert task_base_instance.on_failure == []
    assert isinstance(task_base_instance.result, task_result.TaskResult)
    assert task_base_instance.result.cause is None
    assert task_base_instance.result.value is None
    assert task_base_instance.retry_after is retry_after
    assert task_base_instance.routing_label == (RoutingLabel.PI_PORTAL_CONTROL)
    assert task_base_instance.scheduled is None
    assert task_base_instance.type == TaskType.BASE

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_initialize__vary_routing_label__attributes(
      self,
      concrete_task_base_class: "Type[task_base.TypeGenericTask]",
      mocked_generic_task_args: MockGenericTaskArgs,
      routing_label: RoutingLabel,
  ) -> None:
    task_base_instance = concrete_task_base_class(
        mocked_generic_task_args,
        routing_label=routing_label,
    )

    assert task_base_instance.args == mocked_generic_task_args
    assert task_base_instance.completed is None
    assert isinstance(task_base_instance.created, datetime)
    assert task_base_instance.id is None
    assert task_base_instance.ok is None
    assert task_base_instance.on_success == []
    assert task_base_instance.on_failure == []
    assert isinstance(task_base_instance.result, task_result.TaskResult)
    assert task_base_instance.result.cause is None
    assert task_base_instance.result.value is None
    assert task_base_instance.retry_after == 0
    assert task_base_instance.routing_label == routing_label
    assert task_base_instance.scheduled is None
    assert task_base_instance.type == TaskType.BASE

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
