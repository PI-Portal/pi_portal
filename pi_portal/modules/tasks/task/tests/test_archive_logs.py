"""Test the archive_logs module."""

from pi_portal import config
from pi_portal.modules.tasks import enums
from pi_portal.modules.tasks.task import archive_logs
from pi_portal.modules.tasks.task.shared import archive
from pi_portal.modules.tasks.task.utility.generic_task_test import (
    GenericTaskModuleTest,
)


class TestArchiveLogs(GenericTaskModuleTest):
  """Test the archive_logs module."""

  expected_api_enabled = False
  expected_arg_class = archive_logs.Args
  expected_return_type = None
  expected_type = enums.TaskType.ARCHIVE_LOGS
  mock_args = archive_logs.Args(partition_name="mock_partition")
  module = archive_logs

  def test_import__args_class__attributes(self) -> None:
    assert archive_logs.Args.archival_path == config.PATH_QUEUE_LOG_UPLOAD

  def test_import__args_class__inheritance(self) -> None:
    assert issubclass(
        archive_logs.Args,
        archive.ArchivalTaskArgs,
    )
