"""RenderTemplateStepBase class."""

import abc
from typing import List

from pi_portal.installation.templates import config_file
from pi_portal.modules.system import file_system
from . import system_call_step


class RenderTemplateStepBase(system_call_step.SystemCallBase, abc.ABC):
  """Template render installer step."""

  templates: List[config_file.ConfileFileTemplate]

  def render(self) -> None:
    """Render the configured templates for this step."""

    for template in self.templates:
      self.log.info(
          "Template: '%s' -> '%s' ...", template.source, template.destination
      )
      template.render()
      fs = file_system.FileSystem(template.destination)
      fs.ownership(template.user, template.user)
      fs.permissions(template.permissions)
      self.log.info(
          "Template: '%s' -> '%s' completed.", template.source,
          template.destination
      )
