"""Test the FailedTaskWorker class."""

from datetime import datetime, timedelta, timezone
from io import StringIO
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from pi_portal.modules.python.futures import wait_cm
from pi_portal.modules.tasks.conftest import Interrupt
from pi_portal.modules.tasks.enums import TaskManifests
from .. import failed_task_worker

if TYPE_CHECKING:
  from concurrent.futures import Future


class TestFailedTaskWorker:
  """Test the FailedTaskWorker class."""

  logging_start_up_message = (
      "WARNING - None - None - None - Failed task scheduler is starting ...\n"
  )

  logging_reschedule_message = (
      "INFO - {task.id} - None - None - Rescheduling: '{task}' !\n"
  )

  logging_halt_message = (
      "WARNING - None - None - None - "
      "Failed task scheduler is shutting down ...\n"
  )

  def test_initialize__attributes(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    assert failed_task_worker_instance.log == mocked_task_scheduler.log
    assert failed_task_worker_instance.router == mocked_task_scheduler.router
    assert failed_task_worker_instance.manifest == (
        mocked_task_scheduler.manifests[TaskManifests.FAILED_TASKS]
    )

  def test_start__single_run__no_retryable_tasks__logging(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_sleep: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]

    with pytest.raises(Interrupt):
      failed_task_worker_instance.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message
    assert mocked_sleep.mock_calls == [mock.call(1)] * 2

  def test_start__single_run__retryable_task__not_due__logging(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_sleep: mock.Mock,
      mocked_stream: StringIO,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]
    mocked_task = mock.Mock()
    mocked_task.completed = datetime.now(tz=timezone.utc) + timedelta(days=1)
    mocked_task.retry_after = 1
    mocked_task_scheduler.manifests[TaskManifests.FAILED_TASKS].contents = [
        mocked_task
    ]

    with pytest.raises(Interrupt):
      failed_task_worker_instance.start()

    assert mocked_stream.getvalue() == self.logging_start_up_message
    assert mocked_sleep.mock_calls == [mock.call(1)] * 2

  def test_start__single_run__retryable_task__due__logging(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_sleep: mock.Mock,
      mocked_stream: StringIO,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]
    mocked_task = mock.Mock()
    mocked_task.completed = datetime.now(tz=timezone.utc) - timedelta(days=1)
    mocked_task.retry_after = 1
    mocked_task_scheduler.manifests[TaskManifests.FAILED_TASKS].contents = [
        mocked_task
    ]

    with pytest.raises(Interrupt):
      failed_task_worker_instance.start()

    assert mocked_stream.getvalue() == (
        self.logging_start_up_message +
        self.logging_reschedule_message.format(task=mocked_task)
    )
    assert mocked_sleep.mock_calls == [mock.call(1)] * 2

  def test_start__single_run__retryable_task__due__reschedules(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_sleep: mock.Mock,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    mocked_sleep.side_effect = [None, Interrupt]
    mocked_task = mock.Mock()
    mocked_task.completed = datetime.now(tz=timezone.utc) - timedelta(days=1)
    mocked_task.retry_after = 1
    mocked_task_scheduler.manifests[TaskManifests.FAILED_TASKS].contents = [
        mocked_task
    ]

    with pytest.raises(Interrupt):
      failed_task_worker_instance.start()

    mocked_task_scheduler.router.retry.assert_called_once_with(mocked_task)
    mocked_task_scheduler.manifests[TaskManifests.FAILED_TASKS].\
        remove.assert_called_once_with(mocked_task)

  def test_halt__scheduler_is_running__logging(
      self,
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      failed_task_worker_running: "Future[None]",
      mocked_stream: StringIO,
  ) -> None:
    with wait_cm(failed_task_worker_running):
      failed_task_worker_instance.halt()

    assert mocked_stream.getvalue() == \
        self.logging_start_up_message + self.logging_halt_message

  def test_halt__scheduler_is_running__stops_all_threads(
      self,
      failed_task_worker_running: "Future[None]",
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
  ) -> None:
    with wait_cm(failed_task_worker_running):
      failed_task_worker_instance.halt()

  def test_halt__scheduler_is_running__ensure_minimum_iterations(
      self,
      failed_task_worker_running: "Future[None]",
      failed_task_worker_instance: failed_task_worker.FailedTaskWorker,
      mocked_sleep: mock.Mock,
  ) -> None:
    with wait_cm(failed_task_worker_running):
      failed_task_worker_instance.halt()

    assert mocked_sleep.call_count > 10
