"""TaskBase class."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Generic, List, TypeVar

from pi_portal.modules.tasks.enums import TaskPriority, TaskType
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
      priority: "TaskPriority" = TaskPriority.STANDARD,
      retry_on_error: bool = False,
  ) -> None:
    """:param args: The arguments used by this task instance.
    :param priority: Sets the routing priority for this task.
    :param retry_on_error: Indicates if the task should be retried on an error.
    """
    self.args = args
    self.completed = None
    self.created = datetime.now(tz=timezone.utc)
    self.retry_on_error = retry_on_error
    self.id = None
    self.ok = None
    self.on_success = []
    self.on_failure = []
    self.priority = priority
    self.result = TaskResult[TypeTaskResult]()
    self.scheduled = None

  def __str__(self) -> str:
    return f"Task(id:{self.id}, type:{self.type.value})"
