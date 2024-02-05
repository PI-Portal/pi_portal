"""A task to archive a folder of log files."""

from typing import Any, Dict, Tuple, Type, cast

from pi_portal.modules.tasks.enums import TaskPriority, TaskType
from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase


class MetaTask(type):
  """Typed task classes.

  :params task_type:  The task type for this task class.
  """

  __slots__ = ()

  def __new__(
      mcs: Type[type],
      name: str,
      bases: Tuple[type, ...],
      class_dict: Dict[str, Any],
      task_type: TaskType,
  ) -> "MetaTask":
    new_cls = super(
    ).__new__(  # type: ignore[misc]
        mcs,
        name,
        bases,
        class_dict,
    )
    new_cls.type = task_type
    return cast(
        MetaTask,
        new_cls,
    )

  def __call__(
      cls: "MetaTask",
      args: "TaskArgsBase",
      priority: "TaskPriority" = TaskPriority.STANDARD,
      retry_after: int = 0,
  ) -> "MetaTask":
    return cast(
        MetaTask,
        type.__call__(cls, args, priority, retry_after),
    )
