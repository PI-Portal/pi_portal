"""Processes requests to copy a file on the file system."""

import shutil

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import file_system_copy


class ProcessorClass(
    processor_base.TaskProcessorBase[
        file_system_copy.Args,
        file_system_copy.ReturnType,
    ],
):
  """Processes requests to copy a file on the file system."""

  __slots__ = ()

  type = TaskType.FILE_SYSTEM_COPY

  def _process(
      self,
      task: processor_base.TaskBase[
          file_system_copy.Args,
          file_system_copy.ReturnType,
      ],
  ) -> file_system_copy.ReturnType:
    shutil.copy2(
        src=task.args.source,
        dst=task.args.destination,
    )
