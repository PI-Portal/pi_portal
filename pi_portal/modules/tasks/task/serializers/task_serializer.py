"""TaskSerializer class."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, TypeVar

from pi_portal.modules.tasks.task.bases.task_base import TaskFields

if TYPE_CHECKING:  # pragma: no cover
  from pi_portal.modules.tasks.enums import TaskType
  from pi_portal.modules.tasks.task.bases.task_args_base import TaskArgsBase
  from pi_portal.modules.tasks.task.bases.task_base import TaskBase

TypeTaskResult = TypeVar("TypeTaskResult")
TypeTaskArguments_co = TypeVar(
    "TypeTaskArguments_co",
    bound="TaskArgsBase",
    covariant=True,
)


@dataclass
class SerializedTask(TaskFields[Any]):
  """A serialized representation of a task."""

  __slots__ = (
      "args",
      "on_failure",
      "on_success",
      "type",
  )

  #: The arguments used by this task instance.
  args: "TaskArgsBase"
  #: An array of subsequent jobs to be performed on task failure.
  on_failure: List["SerializedTask"]
  #: An array of subsequent jobs to be performed on task completion.
  on_success: List["SerializedTask"]
  #: The type of task being represented.
  type: "TaskType"

  @classmethod
  def serialize(
      cls,
      task: "TaskBase[TaskArgsBase, Any]",
  ) -> "SerializedTask":
    """Serialize a task into a dataclass.

    :param task: The task to serialize.
    :returns: A task serialized as a dataclass instance.
    """
    definition: Dict[str, Any] = {}

    for slot in cls._get_slots():
      slot_value = getattr(task, slot)
      if not isinstance(slot_value, list):
        definition[slot] = slot_value
      if isinstance(slot_value, list):
        definition[slot] = []
        for sub_task in slot_value:
          definition[slot].append(cls.serialize(sub_task))

    serialized_instance = cls(**definition)
    return serialized_instance

  @classmethod
  def _get_slots(cls) -> List[str]:
    mro_slots = [getattr(klass, '__slots__', ()) for klass in cls.mro()]
    return [slot for slots in mro_slots for slot in slots]
