"""A task to archive a folder of log files."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias
from .shared import archive

ApiEnabled = False
Args = archive.ArchivalTaskArgs
ReturnType: TypeAlias = None
TaskType = enums.TaskType.ARCHIVE_LOGS


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to archive a folder of log files."""
