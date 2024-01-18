"""Tests for the TaskRouterBase class."""

from typing import Dict
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import TaskPriority
from .. import router_base


class TestTaskRouterBase:
  """Tests for the TaskRouterBase class."""

  def test_initialize__attributes__has_all_queues(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
  ) -> None:
    for priority in TaskPriority:
      assert priority in concrete_task_router_base_instance.queues

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_ack__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      mocked_task: mock.Mock,
      priority: TaskPriority,
  ) -> None:
    mocked_task.priority = priority

    concrete_task_router_base_instance.ack(mocked_task)

    mocked_priority_queues[priority].ack.assert_called_once_with(mocked_task)

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_get__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      priority: TaskPriority,
  ) -> None:
    result = concrete_task_router_base_instance.get(priority)

    mocked_priority_queues[priority].get.assert_called_once_with()
    assert result == mocked_priority_queues[priority].get.return_value

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_maintenance__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      priority: TaskPriority,
  ) -> None:
    concrete_task_router_base_instance.maintenance(priority)

    mocked_priority_queues[priority].maintenance.assert_called_once_with()

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_metrics__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      priority: TaskPriority,
  ) -> None:
    result = concrete_task_router_base_instance.metrics(priority)

    mocked_priority_queues[priority].metrics.assert_called_once_with()
    assert result == mocked_priority_queues[priority].metrics.return_value

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_put__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      mocked_task: mock.Mock,
      priority: TaskPriority,
  ) -> None:
    mocked_task.priority = priority

    concrete_task_router_base_instance.put(mocked_task)

    mocked_priority_queues[priority].put.assert_called_once_with(mocked_task)

  @pytest.mark.parametrize("priority", list(TaskPriority))
  def test_retry__vary_priority__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_priority_queues: Dict[TaskPriority, mock.Mock],
      mocked_task: mock.Mock,
      priority: TaskPriority,
  ) -> None:
    mocked_task.priority = priority

    concrete_task_router_base_instance.retry(mocked_task)

    mocked_priority_queues[priority].retry.assert_called_once_with(mocked_task)
