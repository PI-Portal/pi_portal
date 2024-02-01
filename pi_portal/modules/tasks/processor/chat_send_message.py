"""Processes requests to send a chat message."""

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import chat_client
from pi_portal.modules.tasks.task import chat_send_message


class ProcessorClass(
    chat_client.ChatClientMixin,
    processor_base.TaskProcessorBase[
        chat_send_message.Args,
        chat_send_message.ReturnType,
    ],
):
  """Processes requests to send a chat message."""

  __slots__ = ()

  type = TaskType.CHAT_SEND_MESSAGE

  def _process(
      self,
      task: processor_base.TaskBase[
          chat_send_message.Args,
          chat_send_message.ReturnType,
      ],
  ) -> chat_send_message.ReturnType:
    self.client.send_message(task.args.message)
