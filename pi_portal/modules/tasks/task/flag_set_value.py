"""A task to set a flag's value."""

from dataclasses import dataclass

from pi_portal.modules.tasks import enums, flags
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias

ApiEnabled = True


@dataclass
class Args(task_args_base.TaskArgsBase):
  """Arguments for set flag value tasks."""

  flag_name: str
  value: bool

  def __post_init__(self) -> None:
    if not hasattr(flags.Flags, self.flag_name):
      raise ValueError(f"Invalid flag: '{self.flag_name}' !")


ReturnType: TypeAlias = None
TaskType = enums.TaskType.FLAG_SET_VALUE


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to set a flag's value."""
