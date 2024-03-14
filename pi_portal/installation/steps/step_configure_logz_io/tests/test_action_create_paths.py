"""Test the CreateLogzIoPathsAction class."""

import os

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreateLogzIoPathsAction(GenericCreatePathsActionTest):
  """Test the CreateLogzIoPathsAction class."""

  action_class = action_create_paths.CreateLogzIoPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 2

  def test_initialize__attributes__file_beat_config_folder(self) -> None:
    file_beat_config_folder = self.action_class.file_system_paths[0]
    assert file_beat_config_folder.path == os.path.dirname(
        config.PATH_FILEBEAT_CONFIG
    )
    assert file_beat_config_folder.folder is True
    assert file_beat_config_folder.permissions == "755"
    assert file_beat_config_folder.group == "root"
    assert file_beat_config_folder.user == "root"

  def test_initialize__attributes__file_beat_certs_folder(self) -> None:
    file_beat_certs_folder = self.action_class.file_system_paths[1]
    assert file_beat_certs_folder.path == "/etc/pki/tls/certs"
    assert file_beat_certs_folder.folder is True
    assert file_beat_certs_folder.permissions == "755"
    assert file_beat_certs_folder.group == "root"
    assert file_beat_certs_folder.user == "root"
