"""StepRenderTemplates class."""

from typing import List

from pi_portal.installation.templates import (
    config_file,
    configuration_templates,
)
from .bases import system_call_step


class StepRenderTemplates(system_call_step.SystemCallBase):
  """Render the templated configuration."""

  templates: List[config_file.ConfileFileTemplate] = configuration_templates

  def invoke(self) -> None:
    """Render the templated configuration."""

    self.log.info("Rendering templates ...")

    for template in self.templates:
      self.log.info(
          "Template '%s' -> '%s' ...", template.source, template.destination
      )
      template.render()
      self._system_call(f"chown root:root {template.destination}")
      self._system_call(f"chmod 600 {template.destination}")
      self.log.info(
          "Completed '%s' -> '%s'.", template.source, template.destination
      )

    self.log.info("Done rendering templates.")
