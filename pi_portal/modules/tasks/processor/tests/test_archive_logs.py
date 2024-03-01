"""Test the log archival task processor."""

import os
from _thread import LockType
from datetime import datetime, timezone

from pi_portal import config
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor import archive_logs
from pi_portal.modules.tasks.processor.bases import (
    processor_archival,
    processor_base,
)


class TestArchiveLogsTaskProcessor:
  """Test the log archival task processor."""

  def test_initialize__attributes(
      self,
      archive_logs_task_processor_instance: archive_logs.ProcessorClass,
  ) -> None:
    assert archive_logs_task_processor_instance.type == \
        TaskType.ARCHIVE_LOGS

  def test_initialize__mutex(
      self,
      archive_logs_task_processor_instance: archive_logs.ProcessorClass,
  ) -> None:
    assert isinstance(
        archive_logs_task_processor_instance.mutex,
        LockType,
    )

  def test_initialize__inheritance(
      self,
      archive_logs_task_processor_instance: archive_logs.ProcessorClass,
  ) -> None:
    assert isinstance(
        archive_logs_task_processor_instance,
        processor_base.TaskProcessorBase,
    )
    assert isinstance(
        archive_logs_task_processor_instance,
        processor_archival.ArchivalTaskProcessorBaseClass,
    )

  def test_object_name__creates_correct_object_name(
      self,
      archive_logs_task_processor_instance: archive_logs.ProcessorClass,
  ) -> None:
    timestamp = datetime.now().replace(tzinfo=timezone.utc)
    lof_file_name = "mock.log"
    archival_name = os.path.join(
        config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
        f"{timestamp.isoformat()}_{lof_file_name}",
    )

    object_name = archive_logs_task_processor_instance.object_name(
        archival_name
    )

    assert object_name == os.path.join(
        timestamp.date().isoformat(),
        f"{timestamp.timetz().isoformat()}_{lof_file_name}",
    )
