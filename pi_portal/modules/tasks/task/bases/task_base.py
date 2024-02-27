"""TaskBase class."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar

from pi_portal.modules.tasks.config import ROUTING_MATRIX
from pi_portal.modules.tasks.enums import RoutingLabel, TaskType
from typing_extensions import TypeAlias
from .task_fields import TaskFields
from .task_result import TaskResult

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase

TypeTaskArguments_co = TypeVar(
    "TypeTaskArguments_co",
    bound="TaskArgsBase",
    covariant=True,
)
TypeTaskResult = TypeVar("TypeTaskResult")
TypeGenericTask: TypeAlias = "TaskBase[TaskArgsBase, Any]"


# pylint: disable=too-many-instance-attributes
class TaskBase(
    TaskFields[TypeTaskResult],
    Generic[TypeTaskArguments_co, TypeTaskResult],
):
  """A processable unit of work."""

  __slots__ = (
      "args",
      "on_failure",
      "on_success",
  )

  #: The arguments used by this task instance.
  args: "TypeTaskArguments_co"
  #: An array of subsequent jobs to be performed on task failure.
  on_failure: List["TypeGenericTask"]
  #: An array of subsequent jobs to be performed on task completion.
  on_success: List["TypeGenericTask"]
  #: The type of task being represented.
  type: "TaskType" = TaskType.BASE

  # pylint: disable=super-init-not-called
  def __init__(
      self,
      args: "TypeTaskArguments_co",
      retry_after: int = 0,
      routing_label: "Optional[RoutingLabel]" = None
  ) -> None:
    """:param args: The arguments used by this task instance.
    :param retry_after: A positive value in seconds will retry a failed task.
    :param routing_label: Override the routing matrix for this task.
    """
    self.args = args
    self.completed = None
    self.created = datetime.now(tz=timezone.utc)
    self.id = None
    self.ok = None
    self.on_success = []
    self.on_failure = []
    self.result = TaskResult[TypeTaskResult]()
    self.retry_after = retry_after
    self.scheduled = None
    if not routing_label:
      routing_label = ROUTING_MATRIX[self.type]
    self.routing_label = routing_label

  def __str__(self) -> str:
    return f"Task(id:{self.id}, type:{self.type.value})"
