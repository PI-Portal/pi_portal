"""A task to copy a file on the file system."""

from dataclasses import dataclass

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from pi_portal.modules.tasks.task.mixins.arg_file_system_restriction import (
    ArgFileSystemRestrictionMixin,
)
from typing_extensions import TypeAlias

ApiEnabled = True


@dataclass
class Args(ArgFileSystemRestrictionMixin, task_args_base.TaskArgsBase):
  """Arguments for file system copy tasks."""

  file_system_arg_restrictions = {
      "source": [config.LOG_FILE_BASE_FOLDER],
      "destination": [config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,]
  }

  source: str
  destination: str


ReturnType: TypeAlias = None
TaskType = enums.TaskType.FILE_SYSTEM_COPY


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to copy a file on the file system."""
