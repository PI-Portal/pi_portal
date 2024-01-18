"""Processes requests to take a snapshot with a motion camera."""
import logging

from pi_portal.modules.integrations.motion.client import MotionClient
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.task import motion_snapshot


class ProcessorClass(
    processor_base.TaskProcessorBase[
        motion_snapshot.Args,
        motion_snapshot.ReturnType,
    ]
):
  """Processes requests to take a snapshot with a motion camera."""

  __slots__ = ("client",)

  type = TaskType.MOTION_SNAPSHOT

  def __init__(self, log: logging.Logger) -> None:
    super().__init__(log)
    self.client = MotionClient(log)

  def _process(
      self,
      task: processor_base.TaskBase[
          motion_snapshot.Args,
          motion_snapshot.ReturnType,
      ],
  ) -> None:
    self.client.take_snapshot(camera=task.args.camera)
