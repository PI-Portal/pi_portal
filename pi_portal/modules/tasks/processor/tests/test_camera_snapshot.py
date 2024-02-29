"""Test the CameraSnapshotProcessor class."""

import logging
from unittest import mock

from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.camera_snapshot import ProcessorClass
from pi_portal.modules.tasks.processor.mixins import camera_client


class TestCameraSnapshotProcessor:
  """Test the CameraSnapshotProcessor class."""

  def test_initialize__attributes(
      self,
      camera_snapshot_instance: ProcessorClass,
  ) -> None:
    assert camera_snapshot_instance.type == \
        TaskType.CAMERA_SNAPSHOT

  def test_initialize__logger(
      self,
      camera_snapshot_instance: ProcessorClass,
      mocked_task_logger: logging.Logger,
  ) -> None:
    assert isinstance(
        camera_snapshot_instance.log,
        logging.Logger,
    )
    assert camera_snapshot_instance.log == mocked_task_logger

  def test_initialize__inheritance(
      self,
      camera_snapshot_instance: ProcessorClass,
  ) -> None:
    assert isinstance(
        camera_snapshot_instance,
        camera_client.CameraClientMixin,
    )
    assert isinstance(
        camera_snapshot_instance,
        processor_base.TaskProcessorBase,
    )

  def test_process__calls_take_snapshot(
      self,
      camera_snapshot_instance: ProcessorClass,
      mocked_camera_client: mock.Mock,
      mocked_camera_snapshot_task: mock.Mock,
  ) -> None:

    camera_snapshot_instance.process(mocked_camera_snapshot_task)

    mocked_camera_client.assert_called_once_with(camera_snapshot_instance.log)
    mocked_camera_client.return_value.take_snapshot.assert_called_once_with(
        camera=mocked_camera_snapshot_task.args.camera
    )
