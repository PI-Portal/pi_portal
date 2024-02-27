"""Tests for the persist-queue backed task Router."""
import logging
from typing import List
from unittest import mock

from pi_portal.modules.tasks.enums import RoutingLabel
from .. import persist_queue_router


class TestTaskRouter:
  """Test the TaskRouter class."""

  def test_initialize__creates_queues(
      self,
      persist_queue_task_router_instance: persist_queue_router.TaskRouter,
      mocked_router_queue: mock.Mock,
      mocked_queue_logger: logging.Logger,
  ) -> None:
    assert list(persist_queue_task_router_instance.queues.keys()) == \
           list(RoutingLabel)
    assert mocked_router_queue.mock_calls == [
        mock.call(
            mocked_queue_logger,
            routing_label=routing_label,
        ) for routing_label in RoutingLabel
    ]

  def test_initialize__queues_match_priorities(
      self,
      persist_queue_task_router_instance: persist_queue_router.TaskRouter,
      mocked_router_queue: mock.Mock,
      mocked_routed_queues: List[mock.Mock],
  ) -> None:
    for index, mock_call in enumerate(mocked_router_queue.mock_calls):
      routing_label = mock_call.kwargs["routing_label"]
      assert persist_queue_task_router_instance.queues[routing_label] == \
          mocked_routed_queues[index]
