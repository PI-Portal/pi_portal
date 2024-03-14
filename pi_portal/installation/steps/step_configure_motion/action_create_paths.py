"""CreateMotionPathsAction class."""

import os

from pi_portal import config
from pi_portal.installation.actions.action_create_paths import (
    CreatePathsAction,
    FileSystemPath,
)


class CreateMotionPathsAction(CreatePathsAction):
  """Create the required motion paths."""

  file_system_paths = [
      FileSystemPath(
          folder=True,
          path=os.path.dirname(config.PATH_CAMERA_CONFIG),
          permissions="755",
          user="root",
          group="root",
      ),
  ]
