"""Test the MotionSnapshotProcessor class."""

import logging
from unittest import mock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.motion_snapshot import ProcessorClass


class TestMotionSnapshotProcessor:
  """Test the MotionSnapshotProcessor class."""

  def test_initialize__attributes(
      self,
      motion_snapshot_instance: ProcessorClass,
  ) -> None:
    assert motion_snapshot_instance.type == \
        TaskType.MOTION_SNAPSHOT

  def test_initialize__logger(
      self,
      motion_snapshot_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        motion_snapshot_instance.log,
        logging.Logger,
    )
    assert motion_snapshot_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      motion_snapshot_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        motion_snapshot_instance,
        processor_base.TaskProcessorBase,
    )

  def test_process__calls_take_snapshot(
      self,
      motion_snapshot_instance: ProcessorClass,
      mocked_motion_client: mock.Mock,
      mocked_motion_snapshot_task: mock.Mock,
  ) -> None:

    motion_snapshot_instance.process(mocked_motion_snapshot_task)

    mocked_motion_client.assert_called_once_with(motion_snapshot_instance.log)
    mocked_motion_client.return_value.take_snapshot.assert_called_once_with(
        camera=mocked_motion_snapshot_task.args.camera
    )
