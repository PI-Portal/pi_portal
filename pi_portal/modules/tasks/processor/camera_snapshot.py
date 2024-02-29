"""Processes requests to take a snapshot with a camera."""

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import camera_client
from pi_portal.modules.tasks.task import camera_snapshot


class ProcessorClass(
    camera_client.CameraClientMixin, processor_base.TaskProcessorBase[
        camera_snapshot.Args,
        camera_snapshot.ReturnType,
    ]
):
  """Processes requests to take a snapshot with a camera."""

  __slots__ = ()

  type = TaskType.CAMERA_SNAPSHOT

  def _process(
      self,
      task: processor_base.TaskBase[
          camera_snapshot.Args,
          camera_snapshot.ReturnType,
      ],
  ) -> None:
    self.client.take_snapshot(camera=task.args.camera)
