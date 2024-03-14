"""CreateDataPathsAction class."""

from pi_portal import config
from pi_portal.installation.actions.action_create_paths import (
    CreatePathsAction,
    FileSystemPath,
)


class CreateDataPathsAction(CreatePathsAction):
  """Create the required data storage paths."""

  file_system_paths = [
      FileSystemPath(
          folder=True,
          path=config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
      FileSystemPath(
          folder=True,
          path=config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
      FileSystemPath(
          folder=True,
          path=config.PATH_CAMERA_CONTENT,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
      FileSystemPath(
          folder=True,
          path=config.PATH_CAMERA_RUN,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
      FileSystemPath(
          folder=True,
          path=config.PATH_FILEBEAT_CONTENT,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
      FileSystemPath(
          folder=True,
          path=config.PATH_TASKS_SERVICE_DATABASES,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
  ]
