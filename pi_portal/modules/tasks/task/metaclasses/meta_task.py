"""A task to archive a folder of log files."""

from typing import Any, Dict, Optional, Tuple, Type, cast

from pi_portal.modules.tasks.config import ROUTING_MATRIX
from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
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
      retry_after: int = 0,
      routing_label: "Optional[RoutingLabel]" = None
  ) -> "MetaTask":
    if routing_label is None:
      routing_label = ROUTING_MATRIX[getattr(cls, "type")]
    return cast(
        MetaTask,
        type.__call__(cls, args, retry_after, routing_label),
    )
