"""Tests for the persist-queue backed task Router."""
import logging
from typing import List
from unittest import mock

from pi_portal.modules.tasks.enums import TaskPriority
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
           list(TaskPriority)
    assert mocked_router_queue.mock_calls == [
        mock.call(
            mocked_queue_logger,
            priority=priority,
        ) for priority in TaskPriority
    ]

  def test_initialize__queues_match_priorities(
      self,
      persist_queue_task_router_instance: persist_queue_router.TaskRouter,
      mocked_router_queue: mock.Mock,
      mocked_priority_queues: List[mock.Mock],
  ) -> None:
    for index, mock_call in enumerate(mocked_router_queue.mock_calls):
      priority = mock_call.kwargs["priority"]
      assert persist_queue_task_router_instance.queues[priority] == \
          mocked_priority_queues[index]
