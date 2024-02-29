"""A task to remove a file from file system."""

from dataclasses import dataclass

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from typing_extensions import TypeAlias

ApiEnabled = False


@dataclass
class Args(ArgFileSystemRestrictionMixin, task_args_base.TaskArgsBase):
  """Arguments for file system remove tasks."""

  file_system_arg_restrictions = {
      "path":
          [
              config.PATH_CAMERA_CONTENT,
              config.PATH_QUEUE_LOG_UPLOAD,
              config.PATH_QUEUE_VIDEO_UPLOAD,
          ]
  }

  path: str


ReturnType: TypeAlias = None
TaskType = enums.TaskType.FILE_SYSTEM_REMOVE


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to remove a file from the file system."""
