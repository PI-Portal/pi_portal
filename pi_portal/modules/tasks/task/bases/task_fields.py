"""The fields used by all task classes."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pi_portal.modules.tasks.enums import RoutingLabel
from pi_portal.modules.tasks.task.bases.task_result import TaskResult

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
      "result",
      "retry_after",
      "routing_label",
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
  #: Set to None before job completion, afterward returned results.
  result: "TaskResult[TypeTaskResult]"
  #: A positive value in seconds ensures this task will be retried on failure.
  retry_after: int
  #: The routing label for this task.
  routing_label: "RoutingLabel"
  #: Set to None before job completion, afterward returned results.
  scheduled: Optional[datetime]
