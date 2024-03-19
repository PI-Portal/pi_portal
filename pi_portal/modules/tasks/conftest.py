"""Shared test fixtures for the tasks modules tests."""
# pylint: disable=redefined-outer-name

import logging
from dataclasses import dataclass
from io import StringIO
from typing import Dict, List
from unittest import mock

import pytest
from pi_portal.conftest import OptionalFieldsLoggingFilter
from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
from pi_portal.modules.tasks.task.bases import task_args_base


class Interrupt(Exception):
  """Raised during testing to interrupt scheduling loops."""


class TaskLoggingFilter(OptionalFieldsLoggingFilter):

  optional_fields = [
      "cron",
      "manifest",
      "manifest_metrics",
      "processing_time",
      "queue",
      "queue_metrics",
      "scheduled_time",
      "system_metrics",
      "task_id",
      "task_type",
      "total_time",
  ]


@dataclass
class MockGenericTaskArgs(task_args_base.TaskArgsBase):
  value_a: int
  value_b: int
  value_c: int


@pytest.fixture
def mocked_flags() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_generic_task_args() -> MockGenericTaskArgs:
  return MockGenericTaskArgs(
      value_a=1,
      value_b=2,
      value_c=3,
  )


@pytest.fixture
def mocked_task_router(
    mocked_task_router_queues: Dict[RoutingLabel, mock.Mock]
) -> mock.Mock:
  mocked_router = mock.Mock()
  mocked_router.return_value.queues = mocked_task_router_queues
  return mocked_router


@pytest.fixture
def mocked_task_router_queues() -> Dict[RoutingLabel, mock.Mock]:
  mocked_queues: Dict[RoutingLabel, mock.Mock] = {}
  for routing_label in RoutingLabel:
    mocked_queues[routing_label] = mock.Mock()
  return mocked_queues


@pytest.fixture
def mocked_stream() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_task_registry_cron_jobs() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_task_registry(
    mocked_task_registry_cron_jobs: List[mock.Mock]
) -> mock.Mock:
  registry = mock.Mock()
  registry.tasks = {}
  registry.processors = {}
  for task_type in TaskType:
    registry.tasks[task_type] = mock.Mock()
    registry.tasks[task_type].type = task_type
    registry.tasks[task_type].TaskClass.return_value.type = task_type
    registry.processors[task_type] = mock.Mock()
  registry.cron_jobs = mocked_task_registry_cron_jobs
  return registry


@pytest.fixture
def mocked_task_logger(mocked_stream: StringIO) -> logging.Logger:
  logger = logging.getLogger("test")
  handler = logging.StreamHandler(stream=mocked_stream)
  handler.setFormatter(
      logging.
      Formatter('%(levelname)s - %(task_id)s - %(task_type)s - %(message)s')
  )
  logger.handlers = [handler]
  logger.setLevel(logging.DEBUG)
  logger.filters = [TaskLoggingFilter()]
  return logger
