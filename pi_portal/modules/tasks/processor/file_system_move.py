"""Processes requests to move a file on the file system."""
import os
import shutil

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import file_system_move


class ProcessorClass(
    processor_base.TaskProcessorBase[
        file_system_move.Args,
        file_system_move.ReturnType,
    ],
):
  """Processes requests to move a file on the file system."""

  __slots__ = ()

  type = TaskType.FILE_SYSTEM_MOVE

  def _process(
      self,
      task: processor_base.TaskBase[
          file_system_move.Args,
          file_system_move.ReturnType,
      ],
  ) -> file_system_move.ReturnType:
    if os.path.exists(task.args.source):
      shutil.move(
          src=task.args.source,
          dst=task.args.destination,
      )
    else:
      self.recover(task)
