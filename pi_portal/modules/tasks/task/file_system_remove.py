"""A task to remove a file from file system."""

from dataclasses import dataclass

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias

ApiEnabled = False


@dataclass
class Args(task_args_base.TaskArgsBase):
  """Arguments for file system remove tasks."""

  path: str


ReturnType: TypeAlias = None
TaskType = enums.TaskType.FILE_SYSTEM_REMOVE


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to remove a file from the file system."""
