"""RenderTemplateStepBase class."""

import abc
from typing import List

from pi_portal.installation.templates import config_file
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
      self._system_call(
          f"chown {template.user}:{template.user} {template.destination}"
      )
      self._system_call(f"chmod {template.permissions} {template.destination}")
      self.log.info(
          "Template: '%s' -> '%s' completed.", template.source,
          template.destination
      )
