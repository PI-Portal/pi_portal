"""StepRenderTemplates class."""

from typing import List

from pi_portal.installation.templates import common_templates, config_file
from .bases import render_templates_step


class StepRenderConfiguration(render_templates_step.RenderTemplateStepBase):
  """Render the templated configuration."""

  templates: List[config_file.ConfileFileTemplate] = common_templates

  def invoke(self) -> None:
    """Render the templated configuration."""

    self.log.info("Rendering configuration templates ...")
    self.render()
    self.log.info("Done rendering configuration templates.")
