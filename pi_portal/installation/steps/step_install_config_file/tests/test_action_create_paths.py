"""Test the CreatePiPortalPathsAction class."""

import os

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreatePiPortalPathsAction(GenericCreatePathsActionTest):
  """Test the CreatePiPortalPathsAction class."""

  action_class = action_create_paths.CreatePiPortalPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 1

  def test_initialize__attributes__user_config_folder(self) -> None:
    user_config_folder = self.action_class.file_system_paths[0]
    assert user_config_folder.path == os.path.dirname(config.PATH_USER_CONFIG)
    assert user_config_folder.folder is True
    assert user_config_folder.permissions == "755"
    assert user_config_folder.group == "root"
    assert user_config_folder.user == "root"
