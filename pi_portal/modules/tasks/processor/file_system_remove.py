"""Processes requests to remove a file from the file system."""
import os

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import file_system_remove


class ProcessorClass(
    processor_base.TaskProcessorBase[
        file_system_remove.Args,
        file_system_remove.ReturnType,
    ],
):
  """Processes requests to remove a file from the file system."""

  __slots__ = ()

  type = TaskType.FILE_SYSTEM_REMOVE

  def _process(
      self,
      task: processor_base.TaskBase[
          file_system_remove.Args,
          file_system_remove.ReturnType,
      ],
  ) -> file_system_remove.ReturnType:
    if os.path.exists(task.args.path):
      os.remove(task.args.path)
    else:
      self.recover(task)
