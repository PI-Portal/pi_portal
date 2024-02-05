"""Tests for the QueueBase class."""
import logging
from datetime import datetime
from io import StringIO
from unittest import mock

from .. import queue_base


class TestQueueBase:
  """Tests for the QueueBase class."""

  def test_initialize__attributes(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_logger: logging.Logger,
  ) -> None:
    assert concrete_queue_base_instance.log == mocked_queue_logger

  def test_ack__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_task: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    concrete_queue_base_instance.ack(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - "
        f"{concrete_queue_base_instance.priority.value} - "
        f"Ack: '{mocked_task}'!\n"
    )

  def test_ack__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    concrete_queue_base_instance.ack(mocked_task)

    mocked_queue_implementation.ack.assert_called_once_with(mocked_task)

  def test_get__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_task = mocked_queue_implementation.get.return_value

    concrete_queue_base_instance.get()

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - "
        f"{concrete_queue_base_instance.priority.value} - "
        f"Dequeued: '{mocked_task}'!\n"
    )

  def test_get__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
  ) -> None:

    received = concrete_queue_base_instance.get()

    assert received == mocked_queue_implementation.get.return_value

  def test_maintenance__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_stream: StringIO,
  ) -> None:
    concrete_queue_base_instance.maintenance()

    assert mocked_stream.getvalue() == ""

  def test_maintenance__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
  ) -> None:

    concrete_queue_base_instance.maintenance()

    mocked_queue_implementation.maintenance.assert_called_once_with()

  def test_metrics__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_stream: StringIO,
  ) -> None:
    concrete_queue_base_instance.metrics()

    assert mocked_stream.getvalue() == ""

  def test_metrics__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
  ) -> None:
    result = concrete_queue_base_instance.metrics()

    mocked_queue_implementation.metrics.assert_called_once_with()
    assert result == mocked_queue_implementation.metrics.return_value

  def test_put__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_task: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    concrete_queue_base_instance.put(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - "
        f"{concrete_queue_base_instance.priority.value} - "
        f"Enqueued: '{mocked_task}'!\n"
    )

  def test_put__sets_schedule_time(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_task: mock.Mock,
  ) -> None:
    assert not isinstance(mocked_task.sceduled, datetime)

    concrete_queue_base_instance.put(mocked_task)

    assert isinstance(mocked_task.scheduled, datetime)

  def test_put__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    concrete_queue_base_instance.put(mocked_task)

    mocked_queue_implementation.put.assert_called_once_with(mocked_task)

  def test_retry__logging(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_task: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    concrete_queue_base_instance.retry(mocked_task)

    assert mocked_stream.getvalue() == (
        f"DEBUG - {mocked_task.id} - "
        f"{concrete_queue_base_instance.priority.value} - "
        f"Retried: '{mocked_task}'!\n"
    )

  def test_retry__resets_task_attributes(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_task: mock.Mock,
  ) -> None:
    mocked_task.completed = datetime.now()
    mocked_task.ok = False
    mocked_task.result.value = Exception

    concrete_queue_base_instance.retry(mocked_task)

    assert mocked_task.completed is None
    assert mocked_task.ok is None
    assert mocked_task.result.value is None

  def test_retry__underlying_implementation(
      self,
      concrete_queue_base_instance: queue_base.QueueBase,
      mocked_queue_implementation: mock.Mock,
      mocked_task: mock.Mock,
  ) -> None:

    concrete_queue_base_instance.retry(mocked_task)

    mocked_queue_implementation.retry.assert_called_once_with(mocked_task)
