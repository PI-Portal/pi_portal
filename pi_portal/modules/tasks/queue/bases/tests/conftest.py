"""Test fixtures for the queue base classes."""
# pylint: disable=redefined-outer-name

import logging
from typing import Dict, Type, cast
from unittest import mock

import pytest
from pi_portal.modules.tasks.enums import RoutingLabel
from pi_portal.modules.tasks.task.bases.task_base import TypeGenericTask
from .. import queue_base, router_base


@pytest.fixture
def mocked_task() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_queue_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_routed_queues() -> Dict[RoutingLabel, mock.Mock]:
  routing_labels: Dict[RoutingLabel, mock.Mock] = {}
  for routing_label in RoutingLabel:
    routing_labels[routing_label] = mock.Mock()
  return routing_labels


@pytest.fixture
def concrete_queue_base_class(
    mocked_queue_implementation: mock.Mock,
) -> Type[queue_base.QueueBase]:

  class ConcreteQueue(queue_base.QueueBase):

    def _ack(self, task: "TypeGenericTask") -> None:
      mocked_queue_implementation.ack(task)

    def _get(self) -> "TypeGenericTask":
      return cast("TypeGenericTask", mocked_queue_implementation.get())

    def _maintenance(self) -> None:
      mocked_queue_implementation.maintenance()

    def _metrics(self) -> "queue_base.QueueMetrics":
      return cast(
          "queue_base.QueueMetrics",
          mocked_queue_implementation.metrics(),
      )

    def _put(self, task: "TypeGenericTask") -> None:
      mocked_queue_implementation.put(task)

    def _retry(self, task: "TypeGenericTask") -> None:
      mocked_queue_implementation.retry(task)

  return ConcreteQueue


@pytest.fixture
def concrete_queue_base_instance(
    concrete_queue_base_class: Type[queue_base.QueueBase],
    mocked_queue_logger: logging.Logger,
) -> queue_base.QueueBase:
  return concrete_queue_base_class(
      mocked_queue_logger,
      routing_label=RoutingLabel.ARCHIVAL,
  )


@pytest.fixture
def concrete_task_router_base_class(
    mocked_routed_queues: Dict[RoutingLabel, queue_base.QueueBase],
) -> Type[router_base.TaskRouterBase]:

  class ConcreteRouter(router_base.TaskRouterBase):

    def __init__(self, _: logging.Logger) -> None:
      self.queues = mocked_routed_queues

  return ConcreteRouter


@pytest.fixture
def concrete_task_router_base_instance(
    concrete_task_router_base_class: Type[router_base.TaskRouterBase],
    mocked_queue_logger: logging.Logger,
) -> router_base.TaskRouterBase:
  return concrete_task_router_base_class(mocked_queue_logger)
