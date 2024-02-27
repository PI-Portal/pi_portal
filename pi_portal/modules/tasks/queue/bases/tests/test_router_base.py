"""Tests for the TaskRouterBase class."""

from typing import Dict
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import RoutingLabel
from .. import router_base


class TestTaskRouterBase:
  """Tests for the TaskRouterBase class."""

  def test_initialize__attributes__has_all_queues(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
  ) -> None:
    for routing_label in RoutingLabel:
      assert routing_label in concrete_task_router_base_instance.queues

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_ack__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      mocked_task: mock.Mock,
      routing_label: RoutingLabel,
  ) -> None:
    mocked_task.routing_label = routing_label

    concrete_task_router_base_instance.ack(mocked_task)

    mocked_routed_queues[routing_label].ack.assert_called_once_with(mocked_task)

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_get__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      routing_label: RoutingLabel,
  ) -> None:
    result = concrete_task_router_base_instance.get(routing_label)

    mocked_routed_queues[routing_label].get.assert_called_once_with()
    assert result == mocked_routed_queues[routing_label].get.return_value

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_maintenance__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      routing_label: RoutingLabel,
  ) -> None:
    concrete_task_router_base_instance.maintenance(routing_label)

    mocked_routed_queues[routing_label].maintenance.assert_called_once_with()

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_metrics__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      routing_label: RoutingLabel,
  ) -> None:
    result = concrete_task_router_base_instance.metrics(routing_label)

    mocked_routed_queues[routing_label].metrics.assert_called_once_with()
    assert result == mocked_routed_queues[routing_label].metrics.return_value

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_put__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      mocked_task: mock.Mock,
      routing_label: RoutingLabel,
  ) -> None:
    mocked_task.routing_label = routing_label

    concrete_task_router_base_instance.put(mocked_task)

    mocked_routed_queues[routing_label].put.assert_called_once_with(mocked_task)

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_retry__vary_label__selects_correct_queue(
      self,
      concrete_task_router_base_instance: router_base.TaskRouterBase,
      mocked_routed_queues: Dict[RoutingLabel, mock.Mock],
      mocked_task: mock.Mock,
      routing_label: RoutingLabel,
  ) -> None:
    mocked_task.routing_label = routing_label

    concrete_task_router_base_instance.retry(mocked_task)

    mocked_routed_queues[routing_label].retry.assert_called_once_with(
        mocked_task
    )
