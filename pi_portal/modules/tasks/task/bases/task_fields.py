"""The fields used by all task classes."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar, Union

from pi_portal.modules.tasks.enums import TaskPriority

TypeTaskResult = TypeVar("TypeTaskResult")


@dataclass
# pylint: disable=too-many-instance-attributes
class TaskFields(Generic[TypeTaskResult]):
  """The fields used by all task classes."""

  __slots__ = (
      "completed",
      "created",
      "id",
      "ok",
      "priority",
      "result",
      "retry_on_error",
      "scheduled",
  )

  #: The datetime of completion, or None if not complete.
  completed: Optional[datetime]
  #: The datetime of task creation.
  created: datetime
  #: The id (assigned by the queue) for this task.
  id: Any
  #: Set to None before job completion, afterward a boolean job status.
  ok: Optional[bool]
  #: Configure to control task routing, defaults to 'STANDARD'.
  priority: "TaskPriority"
  #: Set to None before job completion, afterward returned results.
  result: Union[Exception, "TypeTaskResult", None]
  #: A boolean indicating if failed jobs should be retried.
  retry_on_error: bool
  #: Set to None before job completion, afterward returned results.
  scheduled: Optional[datetime]
