"""Test the video archival task processor."""

import os
from _thread import LockType

from pi_portal import config
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor import archive_videos
from pi_portal.modules.tasks.processor.bases import (
    processor_archival,
    processor_base,
)


class TestArchiveVideosTaskProcessor:
  """Test the video archival task processor."""

  def test_initialize__attributes(
      self,
      archive_videos_task_processor_instance: archive_videos.ProcessorClass,
  ) -> None:
    assert archive_videos_task_processor_instance.type == \
        TaskType.ARCHIVE_VIDEOS

  def test_initialize__mutex(
      self,
      archive_videos_task_processor_instance: archive_videos.ProcessorClass,
  ) -> None:
    assert isinstance(
        archive_videos_task_processor_instance.mutex,
        LockType,
    )

  def test_initialize__inheritance(
      self,
      archive_videos_task_processor_instance: archive_videos.ProcessorClass,
  ) -> None:
    assert isinstance(
        archive_videos_task_processor_instance,
        processor_base.TaskProcessorBase,
    )
    assert isinstance(
        archive_videos_task_processor_instance,
        processor_archival.ArchivalTaskProcessorBaseClass,
    )

  def test_object_name__creates_correct_object_name(
      self,
      archive_videos_task_processor_instance: archive_videos.ProcessorClass,
  ) -> None:
    base_name = "video.mp4"
    archival_name = os.path.join(
        config.PATH_QUEUE_LOG_UPLOAD,
        base_name,
    )

    object_name = archive_videos_task_processor_instance.object_name(
        archival_name
    )

    assert object_name == base_name
