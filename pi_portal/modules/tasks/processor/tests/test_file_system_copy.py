"""Test the FileSystemCopyProcessor class."""

import logging
from unittest import mock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.file_system_move import ProcessorClass


class TestFileSystemCopyProcessor:
  """Test the FileSystemCopyProcessor class."""

  def test_initialize__attributes(
      self,
      file_system_copy_instance: ProcessorClass,
  ) -> None:
    assert file_system_copy_instance.type == \
        TaskType.FILE_SYSTEM_COPY

  def test_initialize__logger(
      self,
      file_system_copy_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        file_system_copy_instance.log,
        logging.Logger,
    )
    assert file_system_copy_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      file_system_copy_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        file_system_copy_instance,
        processor_base.TaskProcessorBase,
    )

  def test_process__calls_shutil(
      self,
      file_system_copy_instance: ProcessorClass,
      mocked_file_system_src_dst_task: mock.Mock,
      mocked_shutil: mock.Mock,
  ) -> None:
    file_system_copy_instance.process(mocked_file_system_src_dst_task)

    mocked_shutil.copy2.assert_called_once_with(
        src=mocked_file_system_src_dst_task.args.source,
        dst=mocked_file_system_src_dst_task.args.destination,
    )
