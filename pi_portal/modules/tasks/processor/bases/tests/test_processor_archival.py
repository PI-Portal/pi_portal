"""Test the ArchivalTaskProcessorBaseClass class."""
import logging
import os
from io import StringIO
from typing import List, Type, cast
from unittest import mock

import pytest
from pi_portal.modules.integrations.archival import TypeArchivalClient
from pi_portal.modules.integrations.folder import queue
from pi_portal.modules.python import traceback
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.mixins import archival_client
from ..processor_archival import ArchivalTaskProcessorBaseClass
from ..processor_base import TaskProcessorBase


class TestArchivalTaskProcessorBaseClass:
  """Test the ArchivalTaskProcessorBaseClass class."""

  logging__mutex_locked__no_files = "\n".join(
      [
          "DEBUG - {task} - Processing '{type}' ...",
          "INFO - {task} - Mutex is locked, aborting '{type}' cron run ...",
          "DEBUG - {task} - Completed '{type}'!",
      ]
  ) + "\n"

  logging__no_mutex__no_files = "\n".join(
      [
          "DEBUG - {task} - Processing '{type}' ...",
          "DEBUG - {task} - Completed '{type}'!",
      ]
  ) + "\n"

  logging__no_mutex__files = "\n".join(
      [
          "DEBUG - {task} - Processing '{type}' ...",
          "DEBUG - {task} - Uploading '/1/file1' -> 'file1' ...",
          "DEBUG - {task} - Removing '/1/file1' ...",
          "DEBUG - {task} - Uploading '/2/file2' -> 'file2' ...",
          "DEBUG - {task} - Removing '/2/file2' ...",
          "DEBUG - {task} - Uploading '/3/file3' -> 'file3' ...",
          "DEBUG - {task} - Removing '/3/file3' ...",
          "DEBUG - {task} - Completed '{type}'!",
      ]
  ) + "\n"

  logging__no_mutex__files__exception1 = "\n".join(
      [
          "DEBUG - {task} - Processing '{type}' ...",
          "DEBUG - {task} - Uploading '/1/file1' -> 'file1' ...",
          "DEBUG - {task} - Removing '/1/file1' ...",
          "DEBUG - {task} - Uploading '/2/file2' -> 'file2' ...",
          "ERROR - {task} - Failed to upload '/2/file2' ...",
          "ERROR - {task} - Failed: '{type}'!",
          "ERROR - {task} - Exception",
      ]
  ) + "\n"

  logging__no_mutex__files__exception2 = "\n".join(
      [
          "DEBUG - {task} - Processing '{type}' ...",
          "DEBUG - {task} - Uploading '/1/file1' -> 'file1' ...",
          "DEBUG - {task} - Removing '/1/file1' ...",
          "DEBUG - {task} - Uploading '/2/file2' -> 'file2' ...",
          "DEBUG - {task} - Removing '/2/file2' ...",
          "ERROR - {task} - Failed to remove '/2/file2' ...",
          "ERROR - {task} - Failed: '{type}'!",
          "ERROR - {task} - Exception",
      ]
  ) + "\n"

  def test_initialize__attributes(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_mutex: mock.Mock,
  ) -> None:
    assert archival_processor_instance.disk_queue_class == \
        queue.DiskQueueIterator
    assert archival_processor_instance.type == TaskType.BASE
    assert archival_processor_instance.mutex == mocked_mutex

  def test_initialize__archival_client(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_archival_client_class: mock.Mock,
  ) -> None:
    assert archival_processor_instance.archival_client_class == \
         cast(Type[TypeArchivalClient], mocked_archival_client_class)
    assert issubclass(
        archival_processor_instance.archival_client_exception_class, Exception
    )

  def test_initialize__inheritance(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
  ) -> None:
    assert isinstance(
        archival_processor_instance,
        TaskProcessorBase,
    )
    assert isinstance(
        archival_processor_instance,
        archival_client.ArchivalClientMixin,
    )

  def test_initialize__logging(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert archival_processor_instance.log == mocked_task_logger
    assert isinstance(archival_processor_instance.log, logging.Logger)

  @pytest.mark.parametrize("mutex_locked", [
      True,
      False,
  ])
  def test_process__vary_mutex__no_files__creates_disk_queue(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_mutex: mock.MagicMock,
      mutex_locked: bool,
  ) -> None:
    mocked_mutex.locked.return_value = mutex_locked
    mocked_disk_queue_class = mock.Mock(return_value=[])
    archival_processor_instance.disk_queue_class = \
        mocked_disk_queue_class

    archival_processor_instance.process(mocked_archival_task)

    called = mocked_disk_queue_class.mock_calls == \
        [mock.call(mocked_archival_task.args.archival_path)]
    not_called = mocked_disk_queue_class.call_count == 0
    assert called is not mutex_locked
    assert not_called is mutex_locked

  @pytest.mark.parametrize("mutex_locked", [
      True,
      False,
  ])
  def test_process__vary_mutex__no_files__creates_archival_client(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_mutex: mock.MagicMock,
      mutex_locked: bool,
  ) -> None:
    mocked_mutex.locked.return_value = mutex_locked
    mocked_archival_client_class = mock.Mock()
    archival_processor_instance. archival_client_class = \
        mocked_archival_client_class
    archival_processor_instance.disk_queue_class = \
        mock.Mock(return_value=[])

    archival_processor_instance.process(mocked_archival_task)

    called = mocked_archival_client_class.mock_calls == \
        [mock.call(mocked_archival_task.args.partition_name)]
    not_called = mocked_archival_client_class.call_count == 0
    assert called is not mutex_locked
    assert not_called is mutex_locked

  @pytest.mark.parametrize("mutex_locked", [
      True,
      False,
  ])
  def test_process__vary_mutex__no_files__calls_os_remove(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_mutex: mock.MagicMock,
      mocked_os_remove: mock.Mock,
      mutex_locked: bool,
  ) -> None:
    mocked_mutex.locked.return_value = mutex_locked
    archival_processor_instance. archival_client_class = \
        mock.Mock()
    archival_processor_instance. disk_queue_class = \
        mock.Mock(return_value=[])

    archival_processor_instance.process(mocked_archival_task)

    mocked_os_remove.assert_not_called()

  @pytest.mark.parametrize("mutex_locked", [
      True,
      False,
  ])
  def test_process__vary_mutex__no_files__logging(
      self,
      archival_processor_instance: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_mutex: mock.Mock,
      mocked_stream: StringIO,
      mutex_locked: bool,
  ) -> None:
    mocked_mutex.locked.return_value = mutex_locked
    archival_processor_instance.disk_queue_class = \
        mock.Mock(return_value=[])
    values = {
        "type": mocked_archival_task,
        "task": mocked_archival_task.id,
    }

    archival_processor_instance.process(mocked_archival_task)

    mutex_locked_message = mocked_stream.getvalue() == \
        self.logging__mutex_locked__no_files.format(**values)
    mutex_unlocked_message = mocked_stream.getvalue() == \
        self.logging__no_mutex__no_files.format(**values)

    assert mutex_locked_message is mutex_locked
    assert mutex_unlocked_message is not mutex_locked

  def test_process__mutex_unlocked__files__archival_client_uploads(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_client_class: mock.Mock,
      mocked_archival_task: mock.Mock,
      mocked_file_list: List[str],
  ) -> None:
    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_archival_client_class.return_value.upload.mock_calls == [
        mock.call(
            file_name,
            os.path.basename(file_name),
        ) for file_name in mocked_file_list
    ]

  def test_process__mutex_unlocked__files__archival_client_upload__exception1(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_archival_client_class: mock.Mock,
      mocked_file_list: List[str],
  ) -> None:
    mocked_archival_client_class.return_value.upload.side_effect = [
        None,
        archival_processor_instance_with_files.archival_client_exception_class,
        None
    ]

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_archival_client_class.return_value.upload.mock_calls == [
        mock.call(
            file_name,
            os.path.basename(file_name),
        ) for file_name in mocked_file_list[0:2]
    ]

  def test_process__mutex_unlocked__files__archival_client_upload__exception2(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_archival_client_class: mock.Mock,
      mocked_file_list: List[str],
      mocked_os_remove: mock.Mock,
  ) -> None:
    mocked_os_remove.side_effect = [None, OSError, None]

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_archival_client_class.return_value.upload.mock_calls == [
        mock.call(
            file_name,
            os.path.basename(file_name),
        ) for file_name in mocked_file_list[0:2]
    ]

  def test_process__mutex_unlocked__files__calls_os_remove(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_file_list: List[str],
      mocked_os_remove: mock.Mock,
  ) -> None:
    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_os_remove.mock_calls == [
        mock.call(file_name) for file_name in mocked_file_list
    ]

  def test_process__mutex_unlocked__files__calls_os_remove__exception1(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_archival_client_class: mock.Mock,
      mocked_file_list: List[str],
      mocked_os_remove: mock.Mock,
  ) -> None:
    mocked_archival_client_class.return_value.upload.side_effect = [
        None,
        archival_processor_instance_with_files.archival_client_exception_class,
        None
    ]

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_os_remove.mock_calls == [mock.call(mocked_file_list[0])]

  def test_process__mutex_unlocked__files__calls_os_remove__exception2(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_file_list: List[str],
      mocked_os_remove: mock.Mock,
  ) -> None:
    mocked_os_remove.side_effect = [None, OSError, None]

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_os_remove.mock_calls == [
        mock.call(file_name) for file_name in mocked_file_list[0:2]
    ]

  def test_process__mutex_unlocked__files__logging(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    logging_values = {
        "type": mocked_archival_task,
        "task": mocked_archival_task.id,
    }

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_stream.getvalue() == \
        self.logging__no_mutex__files.format(**logging_values)

  def test_process__mutex_unlocked__files__logging__exception1(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_archival_client_class: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_archival_client_class.return_value.upload.side_effect = [
        None,
        archival_processor_instance_with_files.archival_client_exception_class,
        None
    ]
    logging_values = {
        "type": mocked_archival_task,
        "task": mocked_archival_task.id,
    }

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_stream.getvalue() == \
        self.logging__no_mutex__files__exception1.format(**logging_values) + \
        traceback.get_traceback(mocked_archival_task.result.value)

  def test_process__mutex_unlocked__files__logging__exception2(
      self,
      archival_processor_instance_with_files: ArchivalTaskProcessorBaseClass,
      mocked_archival_task: mock.Mock,
      mocked_os_remove: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_os_remove.side_effect = [None, OSError, None]
    logging_values = {
        "type": mocked_archival_task,
        "task": mocked_archival_task.id,
    }

    archival_processor_instance_with_files.process(mocked_archival_task)

    assert mocked_stream.getvalue() == (
        self.logging__no_mutex__files__exception2.format(**logging_values) +
        traceback.get_traceback(mocked_archival_task.result.value).replace(
            "builtins.OSError",
            "OSError",
        )
    )
