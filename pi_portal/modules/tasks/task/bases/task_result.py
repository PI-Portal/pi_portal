"""Task processing result."""
from dataclasses import dataclass
from typing import Any, Generic, Optional, TypeVar, Union

TypeTaskResult = TypeVar("TypeTaskResult")


@dataclass
class TaskResult(Generic[TypeTaskResult]):
  """Task processing result."""

  cause: Optional["TaskResult[Any]"] = None
  value: Union[Exception, None, "TypeTaskResult"] = None
