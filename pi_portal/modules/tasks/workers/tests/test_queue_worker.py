"""Test the QueueWorker class."""
import logging
from io import StringIO
from typing import TYPE_CHECKING
from unittest import mock

import pytest
from pi_portal.modules.python.futures import wait_cm
from pi_portal.modules.tasks.conftest import Interrupt
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.workers.bases.worker_base import WorkerBase
from .. import queue_worker
from .conftest import (
    MockTaskArgs,
    RetryScenario,
    TaskScenario,
    TypeQueueWorkerMocksCreator,
)

if TYPE_CHECKING:
  from concurrent.futures import Future


class TestQueueWorker:
  """Test the QueueWorker class."""

  def test_initialize__attributes(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      mocked_queue: mock.Mock,
      mocked_manifest: mock.Mock,
  ) -> None:
    assert queue_worker_instance.do_not_process == [TaskType.NON_SCHEDULED]
    assert queue_worker_instance.priority == mocked_queue.priority
    assert queue_worker_instance.failed_task_manifest == mocked_manifest

  def test_initialize__logger(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      mocked_worker_logger: logging.Logger,
  ) -> None:
    assert queue_worker_instance.log == mocked_worker_logger
    assert isinstance(
        queue_worker_instance.log,
        logging.Logger,
    )

  def test_initialize__queue(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      mocked_queue: mock.Mock,
  ) -> None:
    assert queue_worker_instance.queue == mocked_queue

  def test_initialize__registry(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      mocked_task_registry: mock.Mock,
  ) -> None:
    assert queue_worker_instance.registry == mocked_task_registry

  def test_initialize__inheritance(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
  ) -> None:
    assert isinstance(queue_worker_instance, WorkerBase)

  def test_start__mocked_consumer__logging(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      monkeypatch: pytest.MonkeyPatch,
      mocked_stream: StringIO,
  ) -> None:
    mocked_consumer = mock.Mock(side_effect=[None, Interrupt])
    monkeypatch.setattr(queue_worker_instance, "consumer", mocked_consumer)

    with pytest.raises(Interrupt):
      queue_worker_instance.start()

    assert mocked_stream.getvalue() == (
        f"WARNING - None - None - {queue_worker_instance.priority.value} - "
        f"Worker thread has started ...\n"
    )

  def test_start__mocked_consumer__calls_consumer(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    mocked_consumer = mock.Mock(side_effect=[None, Interrupt])
    monkeypatch.setattr(queue_worker_instance, "consumer", mocked_consumer)

    with pytest.raises(Interrupt):
      queue_worker_instance.start()

    assert mocked_consumer.mock_calls == [mock.call()] * 2

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.NON_SCHEDULED,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=None,
          ),
      ],
  )
  def test_consumer__processing_sequence__non_scheduled_task(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      queue_worker_processing_sequence: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    mocked_queue.get.return_value = task

    scenario_mocks.instance.consumer()

    assert queue_worker_processing_sequence.mock_calls == [
        mock.call.ack(task),
    ]

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=None,
          ),
      ],
  )
  def test_consumer__processing_sequence__scheduled_task(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      queue_worker_processing_sequence: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    mocked_queue.get.return_value = task

    scenario_mocks.instance.consumer()

    assert queue_worker_processing_sequence.mock_calls == [
        mock.call.processing(task),
        mock.call.ack(task),
        mock.call.success(task),
        mock.call.failure(task),
    ]

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.NON_SCHEDULED,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=None,
          ),
      ],
  )
  def test_consumer__non_scheduled_task__does_not_get_processed(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    mocked_process_class.assert_not_called()

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.NON_SCHEDULED,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=None,
          ),
      ],
  )
  def test_consumer__non_scheduled_task__calls_queue_ack(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    mocked_queue.get.return_value = task

    scenario_mocks.instance.consumer()

    mocked_queue.ack.assert_called_once_with(task)

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=None,
          ),
          TaskScenario(
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=None,
          ),
      ],
  )
  def test_consumer__vary_tasks__creates_correct_processor_class(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    assert scenario_mocks.instance.registry.processors[scenario.task_type] == \
        scenario_mocks.mocked_processor
    mocked_process_class.assert_called_once_with(scenario_mocks.instance.log)
    mocked_process_class.return_value.process.assert_called_once_with(task)

  @pytest.mark.parametrize(
      "scenario",
      [
          RetryScenario(
              retry_after=1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  def test_consumer__vary_tasks__vary_ok__vary_retry__calls_queue_ack(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: RetryScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.completed = task.completed
    task.retry_after = scenario.retry_after
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    mocked_process_class.assert_called_once_with(scenario_mocks.instance.log)
    mocked_queue.ack.assert_called_once_with(task)

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          TaskScenario(
              task_type=TaskType.CHAT_UPLOAD_SNAPSHOT,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  def test_consumer__vary_tasks__vary_ok__vary_retry__on_success_sub_tasks(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    sub_task_mocks = [mock.Mock(), mock.Mock()]
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.retry_after = 0
    setattr(task, "on_success", sub_task_mocks)
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    mocked_process_class.assert_called_once_with(scenario_mocks.instance.log)
    called = mocked_queue.put.mock_calls == list(
        map(
            mock.call,
            sub_task_mocks,
        )
    )
    not_called = mocked_queue.put.call_count == 0
    assert called is scenario.ok
    assert not_called is not scenario.ok

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          TaskScenario(
              task_type=TaskType.CHAT_UPLOAD_SNAPSHOT,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  def test_consumer__vary_tasks__vary_ok__vary_retry__on_failure_sub_tasks(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    sub_task_mocks = [mock.Mock(), mock.Mock()]
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.retry_after = 0
    setattr(task, "on_failure", sub_task_mocks)
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    mocked_process_class.assert_called_once_with(scenario_mocks.instance.log)
    called = mocked_queue.put.mock_calls == list(
        map(
            mock.call,
            sub_task_mocks,
        )
    )
    not_called = mocked_queue.put.call_count == 0
    assert called is not scenario.ok
    assert not_called is scenario.ok

  @pytest.mark.parametrize(
      "scenario",
      [
          TaskScenario(
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          TaskScenario(
              task_type=TaskType.CHAT_UPLOAD_SNAPSHOT,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  @pytest.mark.parametrize(
      "completion_attribute",
      ["on_failure", "on_success"],
  )
  def test_consumer__vary_tasks__vary_ok__vary_sub_tasks__sets_result_cause(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      scenario: TaskScenario,
      completion_attribute: str,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    sub_task_mocks = [mock.Mock(), mock.Mock()]
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.retry_after = 0
    setattr(task, completion_attribute, sub_task_mocks)
    mocked_queue.get.return_value = task

    scenario_mocks.instance.consumer()

    task_created = (
        (scenario.ok and completion_attribute == "on_success")
        or (not scenario.ok and completion_attribute == "on_failure")
    )

    if task_created:
      for sub_task in sub_task_mocks:
        assert sub_task.result.cause == task.result

  @pytest.mark.parametrize(
      "scenario",
      [
          RetryScenario(
              retry_after=1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=True,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  def test_consumer__vary_tasks__vary_ok__vary_retry__updates_manifest(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_manifest: mock.Mock,
      mocked_queue: mock.Mock,
      scenario: RetryScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.retry_after = scenario.retry_after
    mocked_queue.get.return_value = task
    mocked_process_class = scenario_mocks.mocked_processor.ProcessorClass

    scenario_mocks.instance.consumer()

    mocked_process_class.assert_called_once_with(scenario_mocks.instance.log)
    called = mocked_manifest.add.mock_calls == [mock.call(task)]
    not_called = mocked_manifest.add.mock_calls == []
    assert called is (not scenario.ok and scenario.retry_after > 0)
    assert not_called is (scenario.ok or not scenario.retry_after > 0)

  @pytest.mark.parametrize(
      "scenario",
      [
          RetryScenario(
              retry_after=1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.CHAT_UPLOAD_VIDEO,
              task_args=MockTaskArgs(path="/mock/path1"),
              ok=True,
          ),
          RetryScenario(
              retry_after=1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
          RetryScenario(
              retry_after=-1,
              task_type=TaskType.FILE_SYSTEM_REMOVE,
              task_args=MockTaskArgs(path="/mock/path2"),
              ok=False,
          ),
      ],
  )
  def test_consumer__vary_tasks__vary_ok__vary_retry__logging(
      self,
      create_queue_worker_scenario_mocks: TypeQueueWorkerMocksCreator,
      mocked_queue: mock.Mock,
      mocked_stream: StringIO,
      scenario: RetryScenario,
  ) -> None:
    scenario_mocks = create_queue_worker_scenario_mocks(scenario.task_type)
    task = scenario_mocks.task(args=scenario.task_args)
    task.ok = scenario.ok
    task.retry_after = scenario.retry_after
    mocked_queue.get.return_value = task

    scenario_mocks.instance.consumer()

    has_no_retry_logging = mocked_stream.getvalue() == ""
    has_retry_logging = mocked_stream.getvalue() == (
        f"DEBUG - {task.id} - None - "
        f"{scenario_mocks.instance.priority.value} - Failed task '{task}' will "
        f"be rescheduled in {scenario.retry_after} second(s).\n"
    )
    assert has_no_retry_logging is (scenario.ok or scenario.retry_after < 1)
    assert has_retry_logging is (not scenario.ok and scenario.retry_after > 0)

  def test_halt__scheduler_is_running__logging(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      queue_worker_running: "Future[None]",
      mocked_stream: StringIO,
  ) -> None:
    with wait_cm(queue_worker_running):
      queue_worker_instance.halt()

    assert mocked_stream.getvalue() == (
        f"WARNING - None - None - {queue_worker_instance.priority.value} - "
        f"Worker thread has started ...\n"
        f"WARNING - None - None - {queue_worker_instance.priority.value} - "
        f"Worker thread has exited!\n"
    )

  def test_halt__scheduler_is_running__stops_all_threads(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      queue_worker_running: "Future[None]",
  ) -> None:
    with wait_cm(queue_worker_running):
      queue_worker_instance.halt()

  def test_halt__scheduler_is_running__ensure_minimum_iterations(
      self,
      queue_worker_instance: queue_worker.QueueWorker,
      queue_worker_running: "Future[None]",
      mocked_queue: mock.Mock,
  ) -> None:
    with wait_cm(queue_worker_running):
      queue_worker_instance.halt()

    assert mocked_queue.get.call_count > 10
