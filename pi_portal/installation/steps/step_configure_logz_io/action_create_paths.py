"""CreateLogzIoPathsAction class."""

import os

from pi_portal import config
from pi_portal.installation.actions.action_create_paths import (
    CreatePathsAction,
    FileSystemPath,
)


class CreateLogzIoPathsAction(CreatePathsAction):
  """Create the required logz.io integration paths."""

  file_system_paths = [
      FileSystemPath(
          folder=True,
          path=os.path.dirname(config.PATH_FILEBEAT_CONFIG),
          permissions="755",
          user="root",
          group="root",
      ),
      FileSystemPath(
          folder=True,
          path="/etc/pki/tls/certs",
          permissions="755",
          user="root",
          group="root",
      ),
  ]
