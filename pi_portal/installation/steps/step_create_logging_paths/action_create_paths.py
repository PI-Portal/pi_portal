"""CreateLoggingPathsAction class."""

from pi_portal import config
from pi_portal.installation.actions.action_create_paths import (
    CreatePathsAction,
    FileSystemPath,
)


class CreateLoggingPathsAction(CreatePathsAction):
  """Create the required logz.io integration paths."""

  file_system_paths = [
      FileSystemPath(
          folder=True,
          path=config.LOG_FILE_BASE_FOLDER,
          permissions="750",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
  ]
