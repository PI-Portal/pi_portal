"""Test the archive_videos module."""

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import archive_videos
from pi_portal.modules.tasks.task.shared import archive
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestArchiveVideos(GenericTaskModuleTest):
  """Test the archive_videos module."""

  expected_api_enabled = False
  expected_arg_class = archive_videos.Args
  expected_return_type = None
  expected_type = enums.TaskType.ARCHIVE_VIDEOS
  mock_args = archive_videos.Args(partition_name="mock_partition")
  module = archive_videos

  def test_import__args_class__attributes(self) -> None:
    assert archive_videos.Args.archival_path == config.PATH_QUEUE_VIDEO_UPLOAD

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        archive_videos.Args,
        archive.ArchivalTaskArgs,
    )
