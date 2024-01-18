"""Shared resources for chat tasks."""

from dataclasses import dataclass

from pi_portal.modules.tasks.task.bases import task_args_base


@dataclass
class ChatUploadTaskArgs(task_args_base.TaskArgsBase):
  """Arguments for chat upload tasks."""

  path: str
