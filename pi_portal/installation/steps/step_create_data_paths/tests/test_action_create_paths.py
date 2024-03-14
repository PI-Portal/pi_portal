"""Test the CreateDataPathsAction class."""

from pi_portal import config
from ...utility.generate_action_create_paths_test import (
    GenericCreatePathsActionTest,
)
from .. import action_create_paths


class TestCreateDataPathsAction(GenericCreatePathsActionTest):
  """Test the CreateDataPathsAction class."""

  action_class = action_create_paths.CreateDataPathsAction

  def test_initialize__attributes__file_system_paths(self) -> None:
    assert len(self.action_class.file_system_paths) == 6

  def test_initialize__attributes__log_archival_queue(self) -> None:
    log_archival_queue = self.action_class.file_system_paths[0]
    assert log_archival_queue.path == config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD
    assert log_archival_queue.folder is True
    assert log_archival_queue.permissions == "750"
    assert log_archival_queue.group == config.PI_PORTAL_USER
    assert log_archival_queue.user == config.PI_PORTAL_USER

  def test_initialize__attributes__video_archival_queue(self) -> None:
    video_archival_queue = self.action_class.file_system_paths[1]
    assert video_archival_queue.path == (
        config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD
    )
    assert video_archival_queue.folder is True
    assert video_archival_queue.permissions == "750"
    assert video_archival_queue.group == config.PI_PORTAL_USER
    assert video_archival_queue.user == config.PI_PORTAL_USER

  def test_initialize__attributes__camera_content(self) -> None:
    camera_content = self.action_class.file_system_paths[2]
    assert camera_content.path == config.PATH_CAMERA_CONTENT
    assert camera_content.folder is True
    assert camera_content.permissions == "750"
    assert camera_content.group == config.PI_PORTAL_USER
    assert camera_content.user == config.PI_PORTAL_USER

  def test_initialize__attributes__camera_run(self) -> None:
    camera_run = self.action_class.file_system_paths[3]
    assert camera_run.path == config.PATH_CAMERA_RUN
    assert camera_run.folder is True
    assert camera_run.permissions == "750"
    assert camera_run.group == config.PI_PORTAL_USER
    assert camera_run.user == config.PI_PORTAL_USER

  def test_initialize__attributes__filebeat_content(self) -> None:
    filebeat_content = self.action_class.file_system_paths[4]
    assert filebeat_content.path == config.PATH_FILEBEAT_CONTENT
    assert filebeat_content.folder is True
    assert filebeat_content.permissions == "750"
    assert filebeat_content.group == config.PI_PORTAL_USER
    assert filebeat_content.user == config.PI_PORTAL_USER

  def test_initialize__attributes__tasks_service_databases(self) -> None:
    tasks_service_databases = self.action_class.file_system_paths[5]
    assert tasks_service_databases.path == config.PATH_TASKS_SERVICE_DATABASES
    assert tasks_service_databases.folder is True
    assert tasks_service_databases.permissions == "750"
    assert tasks_service_databases.group == config.PI_PORTAL_USER
    assert tasks_service_databases.user == config.PI_PORTAL_USER
