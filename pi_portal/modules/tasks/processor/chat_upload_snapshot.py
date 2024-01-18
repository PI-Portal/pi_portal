"""Processes requests to upload a snapshot to chat."""
import logging
import os

from pi_portal.modules.integrations.slack import SlackClient
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import (
    chat_upload_snapshot,
    file_system_remove,
)


class ProcessorClass(
    processor_base.TaskProcessorBase[
        chat_upload_snapshot.Args,
        chat_upload_snapshot.ReturnType,
    ]
):
  """Processes requests to upload a snapshot to chat."""

  __slots__ = ("client",)

  type = TaskType.CHAT_UPLOAD_SNAPSHOT

  def __init__(self, log: logging.Logger) -> None:
    super().__init__(log)
    self.client = SlackClient()

  def _process(
      self,
      task: processor_base.TaskBase[
          chat_upload_snapshot.Args,
          chat_upload_snapshot.ReturnType,
      ],
  ) -> chat_upload_snapshot.ReturnType:
    if os.path.exists(task.args.path):
      self.client.send_file(task.args.path)
      next_args = file_system_remove.Args(path=task.args.path)
      task.on_success.append(file_system_remove.Task(args=next_args))
    else:
      self.recover(task)
