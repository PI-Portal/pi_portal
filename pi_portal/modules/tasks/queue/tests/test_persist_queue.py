"""Tests for the persist-queue implementation of Queue."""
import logging
import os
from io import StringIO
from typing import Any, Dict, Type
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.tasks.enums import RoutingLabel
from pi_portal.modules.tasks.queue.bases.queue_base import QueueMetrics
from .. import persist_queue
from .conftest import (
    MetricsScenario,
    TypeMetricsScenarioCreator,
    TypeMockRawTask,
)


class TestQueue:
  """Test the Queue class."""

  vendor_queue_call_args: Dict[str, Any] = {
      "block": True,
      "timeout": 1,
      "raw": True,
  }

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_initialize__vary_label__attributes(
      self,
      persist_queue_instance_class: Type[persist_queue.Queue],
      mocked_queue_logger: logging.Logger,
      routing_label: RoutingLabel,
  ) -> None:
    persist_queue_instance = persist_queue_instance_class(
        mocked_queue_logger,
        routing_label=routing_label,
    )

    assert persist_queue_instance.timeout == 2
    # pylint: disable=protected-access
    assert persist_queue_instance._path == (
        os.path.join(
            config.PATH_TASKS_SERVICE_DATABASES,
            routing_label.value,
        )
    )
    assert persist_queue_instance.log == mocked_queue_logger

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_initialize__vary_label__creates_path(
      self,
      persist_queue_instance_class: Type[persist_queue.Queue],
      mocked_os_makedirs: mock.Mock,
      routing_label: RoutingLabel,
  ) -> None:
    persist_queue_instance = persist_queue_instance_class(
        mock.Mock(),
        routing_label=routing_label,
    )

    mocked_os_makedirs.assert_called_once_with(
        # pylint: disable=protected-access
        persist_queue_instance._path,
        exist_ok=True,
    )

  @pytest.mark.parametrize("routing_label", list(RoutingLabel))
  def test_initialize__vary_label__creates_vendor_queue(
      self,
      persist_queue_instance_class: Type[persist_queue.Queue],
      mocked_queue_implementation: mock.Mock,
      routing_label: RoutingLabel,
  ) -> None:
    persist_queue_instance = persist_queue_instance_class(
        mock.Mock(),
        routing_label=routing_label,
    )

    mocked_queue_implementation.assert_called_once_with(
        # pylint: disable=protected-access
        path=persist_queue_instance._path,
        auto_resume=True,
        multithreading=True,
        timeout=persist_queue_instance.timeout,
    )

  def test_ack__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    persist_queue_instance_standard.ack(mocked_task)

    mocked_queue_implementation.return_value.ack.assert_called_once_with(
        id=mocked_task.id
    )

  def test_get__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
  ) -> None:
    mocked_queue_implementation.return_value.get.return_value = mocked_raw_task

    received = persist_queue_instance_standard.get()

    mocked_queue_implementation.return_value.get.called_once_with(
        **self.vendor_queue_call_args
    )
    assert received == mocked_raw_task["data"]
    assert received.id == mocked_raw_task["pqid"]

  def test_get__underlying_implementation__vendor_exception_raised(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
  ) -> None:
    mocked_queue_implementation.return_value.get.side_effect = [
        persist_queue.VendorException, mocked_raw_task
    ]

    received = persist_queue_instance_standard.get()

    mocked_queue_implementation.return_value.get.called_once_with(
        **self.vendor_queue_call_args
    )
    assert received == mocked_raw_task["data"]
    assert received.id == mocked_raw_task["pqid"]

  def test_get__deserialization_error__removes_path(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
      mocked_shutil: mock.Mock,
  ) -> None:
    mocked_queue_implementation.return_value.get.side_effect = [
        AttributeError,
        mocked_raw_task,
    ]

    persist_queue_instance_standard.get()

    mocked_shutil.rmtree.assert_called_once_with(
        # pylint: disable=protected-access
        persist_queue_instance_standard._path
    )

  def test_get__deserialization_error__recreates_path(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_os_makedirs: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
  ) -> None:
    mocked_queue_implementation.return_value.get.side_effect = [
        AttributeError,
        mocked_raw_task,
    ]

    persist_queue_instance_standard.get()

    assert mocked_os_makedirs.mock_calls == [
        mock.call(
            # pylint: disable=protected-access
            persist_queue_instance_standard._path,
            exist_ok=True,
        )
    ] * 2

  def test_get__deserialization_error__recreates_vendor_queue(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
  ) -> None:
    mocked_queue_implementation.return_value.get.side_effect = [
        AttributeError,
        mocked_raw_task,
    ]

    persist_queue_instance_standard.get()

    assert mocked_queue_implementation.mock_calls == [
        mock.call(
            # pylint: disable=protected-access
            path=persist_queue_instance_standard._path,
            auto_resume=True,
            multithreading=True,
            timeout=persist_queue_instance_standard.timeout,
        ),
        mock.call().get(**self.vendor_queue_call_args),
    ] * 2

  def test_get__deserialization_error__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
  ) -> None:
    mocked_queue_implementation.return_value.get.side_effect = [
        AttributeError,
        mocked_raw_task,
    ]

    received = persist_queue_instance_standard.get()

    assert mocked_queue_implementation.return_value.get.mock_calls == [
        mock.call(**self.vendor_queue_call_args),
        mock.call(**self.vendor_queue_call_args),
    ]
    assert received == mocked_raw_task["data"]

  def test_get__deserialization_error__logging(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_raw_task: TypeMockRawTask,
      mocked_stream: StringIO,
  ) -> None:
    label = persist_queue_instance_standard.routing_label.value
    mocked_queue_implementation.return_value.get.side_effect = [
        AttributeError,
        mocked_raw_task,
    ]

    persist_queue_instance_standard.get()

    assert mocked_stream.getvalue() == (
        f"ERROR - None - None - {label} - Fatal error during deserialization!\n"
        f"ERROR - None - None - {label} - "
        "To restore service the queue is being cleared. Tasks have been lost!\n"
        f"DEBUG - {mocked_raw_task['pqid']} - "
        f"{mocked_raw_task['data'].type.value} - "
        f"{label} - Dequeued: '{mocked_raw_task['data']}'!\n"
    )

  def test_maintenance__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
  ) -> None:

    persist_queue_instance_standard.maintenance()

    mocked_queue_implementation.return_value.clear_acked_data.\
        assert_called_once_with()
    mocked_queue_implementation.return_value.shrink_disk_usage. \
        assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario,expected",
      [
          [
              MetricsScenario(
                  files_sizes=[2**16, 2**16, 2**16, 2**16],
                  size=200,
                  acked_count=101,
                  unacked_count=99,
              ),
              QueueMetrics(
                  length=200,
                  acked_length=101,
                  unacked_length=99,
                  storage=0.25,
              ),
          ],
          [
              MetricsScenario(
                  files_sizes=[2**18, 2**19],
                  size=203,
                  acked_count=102,
                  unacked_count=101,
              ),
              QueueMetrics(
                  length=203,
                  acked_length=102,
                  unacked_length=101,
                  storage=0.75,
              ),
          ],
      ],
  )
  def test_metrics__underlying_implementation(
      self,
      persist_queue_instance_with_metrics_mocks: persist_queue.Queue,
      persist_queue_metrics_scenario_creator: TypeMetricsScenarioCreator,
      scenario: MetricsScenario,
      expected: QueueMetrics,
  ) -> None:

    persist_queue_metrics_scenario_creator(scenario)

    results = persist_queue_instance_with_metrics_mocks.metrics()

    assert results == expected

  def test_put__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    persist_queue_instance_standard.put(mocked_task)

    mocked_queue_implementation.return_value.put.assert_called_once_with(
        mocked_task
    )

  def test_retry__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    persist_queue_instance_standard.retry(mocked_task)

    mocked_queue_implementation.return_value.nack.assert_called_once_with(
        id=mocked_task.id
    )

  def test_raw__underlying_implementation(
      self,
      persist_queue_instance_standard: persist_queue.Queue,
      mocked_queue_implementation: mock.Mock,
  ) -> None:

    received = persist_queue_instance_standard.raw()

    assert received == mocked_queue_implementation.return_value
