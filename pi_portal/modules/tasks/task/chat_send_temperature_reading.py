"""A task to send the latest temperature reading via the chat client."""

from dataclasses import dataclass

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_args_base, task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias

ApiEnabled = True


@dataclass
class Args(task_args_base.TaskArgsBase):
  """Arguments for chat send temperature reading tasks."""

  header: str


ReturnType: TypeAlias = None
TaskType = enums.TaskType.CHAT_SEND_TEMPERATURE_READING


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to send the latest temperature reading via the chat client."""
