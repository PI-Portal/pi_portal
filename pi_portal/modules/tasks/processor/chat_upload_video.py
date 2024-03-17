"""Processes requests to upload a video to chat."""
import os

from pi_portal import config
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import chat_client
from pi_portal.modules.tasks.task import chat_upload_video, file_system_move


class ProcessorClass(
    chat_client.ChatClientMixin,
    processor_base.TaskProcessorBase[
        chat_upload_video.Args,
        chat_upload_video.ReturnType,
    ],
):
  """Processes requests to upload a video to chat."""

  __slots__ = ()

  recovery_archival_suffix = "-RECOVERED"
  type = TaskType.CHAT_UPLOAD_VIDEO

  def _process(
      self,
      task: processor_base.TaskBase[
          chat_upload_video.Args,
          chat_upload_video.ReturnType,
      ],
  ) -> chat_upload_video.ReturnType:
    archival_path = os.path.join(
        config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
        os.path.basename(task.args.path),
    )
    exists_source = os.path.exists(task.args.path)
    exists_destination = os.path.exists(archival_path)

    if not exists_source:
      # Partial failure: has already been moved
      self.recover(task)
      return

    if exists_source and not exists_destination:
      # pylint: disable=duplicate-code
      self.log.debug(
          "Uploading: '%s' -> 'CHAT' ...",
          task.args.path,
          extra={
              "task_id": task.id,
              "task_type": task.type.value,
          },
      )
      self.client.send_file(task.args.path, task.args.description)

    if exists_destination:
      archival_path = self._recovery_archival_path(archival_path)
      self.recover(task)

    next_args = file_system_move.Args(
        source=task.args.path,
        destination=archival_path,
    )
    task.on_success.append(file_system_move.Task(args=next_args))

  def _recovery_archival_path(self, path: str) -> str:
    name, ext = os.path.splitext(os.path.basename(path))
    recovery_archival_path = os.path.join(
        config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
        name + self.recovery_archival_suffix + ext
    )
    return recovery_archival_path
