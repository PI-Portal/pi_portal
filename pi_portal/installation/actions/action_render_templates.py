"""RenderTemplatesAction class."""

from typing import List

from pi_portal.installation.templates import config_file
from pi_portal.modules.system import file_system
from .bases import base_action


class RenderTemplatesAction(base_action.ActionBase):
  """Render and secure the configured templates."""

  templates: List[config_file.ConfileFileTemplate]

  def invoke(self) -> None:
    """Render and secure the configured templates."""

    for template in self.templates:
      self.log.info(
          "Template: '%s' -> '%s' ...",
          template.source,
          template.destination,
      )
      template.render()
      fs = file_system.FileSystem(template.destination)
      fs.ownership(template.user, template.user)
      fs.permissions(template.permissions)
      self.log.info(
          "Template: '%s' -> '%s' completed.",
          template.source,
          template.destination,
      )
