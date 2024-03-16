"""RenderTemplatesAction class."""

import dataclasses
from typing import Any, Dict, List

from pi_portal.installation.templates import config_file
from pi_portal.modules.system import file_system
from .bases import base_action


@dataclasses.dataclass
class FileSystemTemplate:
  """Represents a config template on the file system.

  :param source: A boolean indicating a folder should be created.
  :param destination: The local path that should be created path.
  :param permissions: The file permissions to set on the created path.
  :param user: The linux user to set as the owner of the created path.
  :param group: The linux user to set as the group of the created path.
  :param context: Optional additional context you wish to pass to the template.
  """

  source: str
  destination: str
  permissions: str
  group: str
  user: str
  context: Dict[str, Any] = dataclasses.field(default_factory=lambda: {})


class RenderTemplatesAction(base_action.ActionBase):
  """Render and secure the configured templates."""

  templates: List[FileSystemTemplate]

  def invoke(self) -> None:
    """Render and secure the configured templates."""

    for template in self.templates:
      self.log.info(
          "Template: '%s' -> '%s' ...",
          template.source,
          template.destination,
      )

      config_file_template = config_file.ConfileFileTemplate(
          source=template.source,
          destination=template.destination,
      )
      config_file_template.context.update(template.context)
      config_file_template.render()

      fs = file_system.FileSystem(template.destination)
      fs.ownership(template.user, template.group)
      fs.permissions(template.permissions)

      self.log.info(
          "Template: '%s' -> '%s' completed.",
          template.source,
          template.destination,
      )
