"""A task to move a file on the file system."""

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
  """Arguments for file system move tasks."""

  file_system_arg_restrictions = {
      "source": [config.PATH_CAMERA_CONTENT],
      "destination":
          [
              config.PATH_QUEUE_LOG_UPLOAD,
              config.PATH_QUEUE_VIDEO_UPLOAD,
          ]
  }

  source: str
  destination: str


ReturnType: TypeAlias = None
TaskType = enums.TaskType.FILE_SYSTEM_MOVE


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to move a file on the file system."""
