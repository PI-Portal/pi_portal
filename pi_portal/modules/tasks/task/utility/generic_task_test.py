"""A generic test suite for task modules."""

from types import ModuleType
from typing import TYPE_CHECKING, Any, Type

import pytest
from pi_portal.modules.tasks import enums, schema
from pi_portal.modules.tasks.config import ROUTING_MATRIX

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase


class GenericTaskModuleTest:
  """A generic test suite for task modules."""

  expected_api_enabled: bool
  expected_arg_class: "Type[TaskArgsBase]"
  expected_return_type: Any
  expected_type: "enums.TaskType"
  mock_args: "TaskArgsBase"
  module: "ModuleType"

  def test_import__module__attributes(self) -> None:
    assert isinstance(self.module, schema.TaskModule)

    assert self.module.ApiEnabled == self.expected_api_enabled
    assert self.module.Args == self.expected_arg_class
    assert self.module.ReturnType == self.expected_return_type
    assert self.module.Task == self.module.Task
    assert self.module.TaskType == self.expected_type

  def test_import__task__defaults__attributes(self) -> None:
    instance = self.module.Task(self.mock_args)

    assert instance.args == self.mock_args
    assert instance.retry_after == 0
    assert instance.routing_label == ROUTING_MATRIX[self.expected_type]
    assert instance.type == self.expected_type

  @pytest.mark.parametrize("retry_after", [0, 1])
  def test_import__task__vary_retry_after__attributes(
      self,
      retry_after: int,
  ) -> None:
    instance = self.module.Task(
        self.mock_args,
        retry_after=retry_after,
    )

    assert instance.args == self.mock_args
    assert instance.type == self.expected_type
    assert instance.retry_after == retry_after
    assert instance.routing_label == ROUTING_MATRIX[self.expected_type]

  @pytest.mark.parametrize("routing_label", list(enums.RoutingLabel))
  def test_import__task__vary_routing_label__attributes(
      self, routing_label: enums.RoutingLabel
  ) -> None:
    instance = self.module.Task(
        self.mock_args,
        routing_label=routing_label,
    )

    assert instance.args == self.mock_args
    assert instance.type == self.expected_type
    assert instance.retry_after == 0
    assert instance.routing_label == routing_label
