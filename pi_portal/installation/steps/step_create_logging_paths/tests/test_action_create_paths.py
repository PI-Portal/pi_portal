"""Test the CreateLoggingPathsAction class."""

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreateLoggingPathsAction(GenericCreatePathsActionTest):
  """Test the CreateLoggingPathsAction class."""

  action_class = action_create_paths.CreateLoggingPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 1

  def test_initialize__attributes__log_file_base_folder(self) -> None:
    log_file_base_folder = self.action_class.file_system_paths[0]
    assert log_file_base_folder.path == config.LOG_FILE_BASE_FOLDER
    assert log_file_base_folder.folder is True
    assert log_file_base_folder.permissions == "750"
    assert log_file_base_folder.group == config.PI_PORTAL_USER
    assert log_file_base_folder.user == config.PI_PORTAL_USER
