"""Test the archive_videos module."""

from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import archive_videos
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestArchiveVideos(GenericTaskModuleTest):
  """Test the archive_videos module."""

  expected_api_enabled = False
  expected_arg_class = archive_videos.Args
  expected_return_type = None
  expected_type = enums.TaskType.ARCHIVE_VIDEOS
  mock_args = archive_videos.Args(
      archival_path="/var/lib/motion/mock.mp4",
      partition_name="mock_partition",
  )
  module = archive_videos
