"""A task to upload a snapshot to the chat client."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task.bases import task_base
from pi_portal.modules.tasks.task.metaclasses.meta_task import MetaTask
from typing_extensions import TypeAlias
from .shared import chat

ApiEnabled = True
Args = chat.ChatUploadTaskArgs
ReturnType: TypeAlias = None
TaskType = enums.TaskType.CHAT_UPLOAD_VIDEO


class Task(
    task_base.TaskBase[Args, ReturnType],
    metaclass=MetaTask,
    task_type=TaskType,
):
  """A task to upload a video to the chat client."""
