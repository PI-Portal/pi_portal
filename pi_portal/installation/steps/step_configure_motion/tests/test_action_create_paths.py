"""Test the CreateMotionPathsAction class."""

import os

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreateMotionPathsAction(GenericCreatePathsActionTest):
  """Test the CreateMotionPathsAction class."""

  action_class = action_create_paths.CreateMotionPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 1

  def test_initialize__attributes__camera_config_folder(self) -> None:
    camera_config_folder = self.action_class.file_system_paths[0]
    assert camera_config_folder.path == os.path.dirname(
        config.PATH_CAMERA_CONFIG
    )
    assert camera_config_folder.folder is True
    assert camera_config_folder.permissions == "755"
    assert camera_config_folder.group == "root"
    assert camera_config_folder.user == "root"
