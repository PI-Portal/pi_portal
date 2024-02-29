"""StepConfigureMotion class."""

from typing import List

from pi_portal.installation.templates import config_file, motion_templates
from pi_portal.modules.configuration import state
from .bases import render_templates_step


class StepConfigureMotion(render_templates_step.RenderTemplateStepBase):
  """Render the motion configuration."""

  templates: List[config_file.ConfileFileTemplate] = motion_templates

  def invoke(self) -> None:
    """Render the templated configuration."""

    self.log.info("Rendering motion configuration ...")
    self.generate_camera_templates()
    self.render()
    self.log.info("Done rendering motion configuration.")

  def generate_camera_templates(self) -> None:
    """Generate config templates for each camera in user configuration."""

    user_config = state.State().user_config

    for index0, camera in enumerate(user_config['CAMERA']["MOTION"]["CAMERAS"]):
      index = index0 + 1
      self.log.info(
          "Creating template for '%s' ...",
          camera["DEVICE"],
      )
      camera_config_file = config_file.ConfileFileTemplate(
          source='motion/camera.conf',
          destination=f'/etc/motion/camera{index}.conf',
          permissions="600",
          user="root",
      )
      camera_config_file.context["CAMERA"] = camera
      camera_config_file.context["CAMERA"]["NAME"] = f"CAMERA-{index}"
      camera_config_file.context["CAMERA"]["ID"] = index
      self.templates.append(camera_config_file)
