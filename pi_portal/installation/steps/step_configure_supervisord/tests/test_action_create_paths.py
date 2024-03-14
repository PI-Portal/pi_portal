"""Test the CreateSupervisordPathsAction class."""

import os

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreateSupervisordPathsAction(GenericCreatePathsActionTest):
  """Test the CreateSupervisordPathsAction class."""

  action_class = action_create_paths.CreateSupervisordPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 1

  def test_initialize__attributes__supervisord_config_folder(self) -> None:
    supervisord_config_folder = self.action_class.file_system_paths[0]
    assert supervisord_config_folder.path == os.path.dirname(
        config.PATH_SUPERVISOR_CONFIG
    )
    assert supervisord_config_folder.folder is True
    assert supervisord_config_folder.permissions == "755"
    assert supervisord_config_folder.group == "root"
    assert supervisord_config_folder.user == "root"
