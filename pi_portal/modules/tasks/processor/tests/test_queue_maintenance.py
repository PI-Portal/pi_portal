"""Test the QueueMaintenanceProcessor class."""

import logging
from io import StringIO
from unittest import mock

from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.queue_maintenance import ProcessorClass


class TestQueueMaintenanceProcessor:
  """Test the QueueMaintenanceProcessor class."""

  log_message_prefix = (
      "DEBUG - {task.id} - {task.type.value} - None - "
      "Processing: '{task}' ...\n"
  )
  log_message_maintenance = (
      "WARNING - {task.id} - {task.type.value} - {queue} - "
      "Performing maintenance on the '{queue}' task queue ...\n"
  )
  log_message_suffix = (
      "DEBUG - {task.id} - {task.type.value} - None - Completed: '{task}'!\n"
      "DEBUG - {task.id} - {task.type.value} - None - Task Timing: '{task}'.\n"
  )

  def test_initialize__attributes(
      self,
      queue_maintenance_instance: ProcessorClass,
  ) -> None:
    assert queue_maintenance_instance.type == \
        TaskType.QUEUE_MAINTENANCE

  def test_initialize__logger(
      self,
      queue_maintenance_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        queue_maintenance_instance.log,
        logging.Logger,
    )
    assert queue_maintenance_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      queue_maintenance_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        queue_maintenance_instance,
        processor_base.TaskProcessorBase,
    )

  def test_process__logging(
      self,
      queue_maintenance_instance: ProcessorClass,
      mocked_stream: StringIO,
      mocked_task_router: mock.Mock,
      mocked_queue_no_args_task: mock.Mock,
  ) -> None:
    mocked_task_router.queues = {
        routing_label: mock.Mock() for routing_label in RoutingLabel
    }

    queue_maintenance_instance.process(mocked_queue_no_args_task)

    assert mocked_stream.getvalue() == (
        self.log_message_prefix.format(task=mocked_queue_no_args_task) +
        "".join(
            [
                self.log_message_maintenance.format(
                    task=mocked_queue_no_args_task,
                    queue=routing_label.value,
                ) for routing_label in RoutingLabel
            ]
        ) + self.log_message_suffix.format(task=mocked_queue_no_args_task)
    )

  def test_process__calls_queue_maintenance(
      self,
      queue_maintenance_instance: ProcessorClass,
      mocked_queue_no_args_task: mock.Mock,
      mocked_task_router: mock.Mock,
  ) -> None:
    mocked_task_router.queues = {
        routing_label: mock.Mock() for routing_label in RoutingLabel
    }

    queue_maintenance_instance.process(mocked_queue_no_args_task)

    for mocked_queue in mocked_task_router.queues.values():
      mocked_queue.maintenance.assert_called_once_with()
