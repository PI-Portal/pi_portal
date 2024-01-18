"""A placeholder for a task that shouldn't be scheduled."""

from dataclasses import dataclass

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias

ApiEnabled = False


@dataclass
class Args(task_args_base.TaskArgsBase):
  """Task has no arguments."""


ReturnType: TypeAlias = None
TaskType = enums.TaskType.NON_SCHEDULED


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A placeholder for a task that shouldn't be scheduled."""
