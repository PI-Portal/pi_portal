"""A task to manage a supervisor process."""

from dataclasses import dataclass
from typing import Literal

from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias

ApiEnabled = False


@dataclass
class Args(task_args_base.TaskArgsBase):
  """Arguments for supervisor process tasks."""

  process: ProcessList
  requested_state: Literal[ProcessStatus.STOPPED, ProcessStatus.RUNNING]


ReturnType: TypeAlias = None
TaskType = enums.TaskType.SUPERVISOR_PROCESS


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to manage a supervisor process."""
