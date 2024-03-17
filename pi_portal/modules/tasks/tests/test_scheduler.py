"""Test the TaskScheduler class."""

import logging
from io import StringIO
from typing import List
from unittest import mock

from pi_portal.modules.mixins import write_archived_log_file
from pi_portal.modules.python.mock import CallType
from pi_portal.modules.tasks.enums import TaskManifests, TaskType
from .. import scheduler
from .conftest import MOCKED_CONFIG


class TestTaskScheduler:
  """Test the TaskScheduler class."""

  logging_startup_message = (
      "WARNING - None - None - None - Task scheduler is starting ...\n"
      "WARNING - None - None - None - Creating the '{manifest.value}' "
      "manifest ...\n"
      "WARNING - None - None - None - Creating the cron scheduler ...\n"
      "WARNING - None - None - None - Creating the failed task scheduler ...\n"
  ) + "".join(
      [
          (
              "WARNING - None - None - {routing_label.value} - "
              "Creating the '{routing_label.value}' queue worker pool ...\n"
          ).format(routing_label=routing_label)
          for routing_label in MOCKED_CONFIG
      ]
  )

  def test_initialize__attributes(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
  ) -> None:
    assert task_scheduler_instance.managed_workers == []
    assert task_scheduler_instance.manifests == {}

  def test_initialize__logger(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_task_logger: mock.Mock,
  ) -> None:
    assert task_scheduler_instance.log == mocked_task_logger
    assert isinstance(
        task_scheduler_instance.log,
        logging.Logger,
    )

  def test_initialize__creates_task_router(
      self,
      task_scheduler_instance_with_logger: scheduler.TaskScheduler,
      mocked_task_router: mock.Mock,
  ) -> None:
    assert task_scheduler_instance_with_logger.router == \
        mocked_task_router.return_value
    mocked_task_router.assert_called_once_with(
        task_scheduler_instance_with_logger.log
    )

  def test_initialize__creates_registry(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_task_registry_factory: mock.Mock,
  ) -> None:
    assert task_scheduler_instance.registry == \
        mocked_task_registry_factory.return_value.create.return_value
    mocked_task_registry_factory.assert_called_once_with()
    mocked_task_registry_factory.return_value.create.assert_called_once_with()

  def test_initialize__inheritance(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
  ) -> None:
    assert isinstance(
        task_scheduler_instance,
        write_archived_log_file.ArchivedLogFileWriter,
    )

  def test_start__logging(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_stream: StringIO,
  ) -> None:
    task_scheduler_instance.start()

    assert mocked_stream.getvalue() == self.logging_startup_message.format(
        manifest=TaskManifests.FAILED_TASKS
    )

  def test_start__creates_manifests(
      self, task_scheduler_instance: scheduler.TaskScheduler,
      mocked_manifest_factory: mock.Mock, mocked_manifests: List[mock.Mock]
  ) -> None:
    task_scheduler_instance.start()

    mocked_manifest_factory.create.assert_called_once_with(
        TaskManifests.FAILED_TASKS
    )
    assert task_scheduler_instance.manifests[TaskManifests.FAILED_TASKS] == \
        mocked_manifests[0]
    assert len(task_scheduler_instance.manifests) == 1

  def test_start__creates_and_starts_cron_worker(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_worker_cron: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    mocked_worker_cron.assert_called_once_with(task_scheduler_instance)
    mocked_worker_cron.return_value.start.assert_called_once_with()

  def test_start__creates_and_starts_failed_task_worker(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_worker_failed_tasks: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    mocked_worker_failed_tasks.assert_called_once_with(task_scheduler_instance)
    mocked_worker_failed_tasks.return_value.start.assert_called_once_with()

  def test_start__creates_and_starts_queue_workers(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_worker_queue: mock.Mock,
  ) -> None:
    expected_worker_init_calls: List[CallType] = []

    task_scheduler_instance.start()

    for routing_label, count in MOCKED_CONFIG.items():
      expected_worker_init_calls += [
          mock.call(
              task_scheduler_instance,
              routing_label,
          ),
      ] * count
    assert mocked_worker_queue.mock_calls == (
        expected_worker_init_calls +
        [mock.call().start()] * sum(MOCKED_CONFIG.values())
    )

  def test_start__stores_managed_workers(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_worker_cron: mock.Mock,
      mocked_worker_failed_tasks: mock.Mock,
      mocked_worker_queue: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    assert task_scheduler_instance.managed_workers[0] == \
        mocked_worker_cron.return_value
    assert task_scheduler_instance.managed_workers[1] == \
           mocked_worker_failed_tasks.return_value
    for worker in task_scheduler_instance.managed_workers[2:]:
      assert worker == mocked_worker_queue.return_value

  def test_halt__scheduler_has_started__logging(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_stream: StringIO,
  ) -> None:
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    assert mocked_stream.getvalue() == (
        self.logging_startup_message.format(
            manifest=TaskManifests.FAILED_TASKS
        ) + "WARNING - None - None - None - Task scheduler is shutting "
        "down ...\n"
    )

  def test_halt__scheduler_has_started__halts_all_managed_workers(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_worker_cron: mock.Mock,
      mocked_worker_failed_tasks: mock.Mock,
      mocked_worker_queue: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    mocked_worker_cron.return_value.halt.assert_called_once_with()
    mocked_worker_failed_tasks.return_value.halt.assert_called_once_with()
    assert mocked_worker_queue.return_value.halt.mock_calls == [
        mock.call()
    ] * sum(MOCKED_CONFIG.values())

  def test_halt__scheduler_has_started__creates_unblocking_tasks(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_task_router: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    assert mocked_task_router.return_value.put.call_count == sum(
        MOCKED_CONFIG.values()
    )
    for call in mocked_task_router.return_value.put.mock_calls:
      task = call.args[0]
      assert task.type == TaskType.NON_SCHEDULED

  def test_halt__scheduler_has_started__creates_tasks_with_correct_attributes(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_task_registry: mock.Mock,
  ) -> None:
    arg_class = mocked_task_registry.tasks[TaskType.NON_SCHEDULED].ArgClass
    task_class = mocked_task_registry.tasks[TaskType.NON_SCHEDULED].TaskClass
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    index = 0
    for routing_label, count in MOCKED_CONFIG.items():
      for call in task_class.mock_calls[index:count]:
        assert call == mock.call(
            args=arg_class.return_value,
            routing_label=routing_label,
        )
      index += count

  def test_halt__scheduler_has_started__routes_all_tasks(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_task_router: mock.Mock,
  ) -> None:
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    assert mocked_task_router.return_value.put.call_count == sum(
        MOCKED_CONFIG.values()
    )

  def test_halt__scheduler_has_started__closes_all_manifests(
      self,
      task_scheduler_instance: scheduler.TaskScheduler,
      mocked_manifests: List[mock.Mock],
  ) -> None:
    task_scheduler_instance.start()

    task_scheduler_instance.halt()

    for manifest in mocked_manifests:
      manifest.close.assert_called_once_with()
