"""RenderMotionTemplatesAction class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    RenderTemplatesAction,
)
from pi_portal.installation.templates.config_file import ConfileFileTemplate
from pi_portal.modules.configuration import state


class RenderMotionTemplatesAction(RenderTemplatesAction):
  """Render the required motion templates."""

  templates = [
      ConfileFileTemplate(
          source='motion/motion.conf',
          destination=config.PATH_CAMERA_CONFIG,
          permissions="600",
          user=config.PI_PORTAL_USER,
      ),
  ]

  def invoke(self) -> None:
    """Render the required motion templates."""

    self.generate_camera_templates()
    super().invoke()

  def generate_camera_templates(self) -> None:
    """Generate config templates for each camera in user configuration."""

    user_config = state.State().user_config

    for index0, camera in enumerate(user_config['CAMERA']["MOTION"]["CAMERAS"]):
      index = index0 + 1
      self.log.info(
          "Creating template for '%s' ...",
          camera["DEVICE"],
      )
      camera_config_file = ConfileFileTemplate(
          source='motion/camera.conf',
          destination=f'/etc/motion/camera{index}.conf',
          permissions="600",
          user=config.PI_PORTAL_USER,
      )
      camera_config_file.context["CAMERA"] = camera
      camera_config_file.context["CAMERA"]["NAME"] = f"CAMERA-{index}"
      camera_config_file.context["CAMERA"]["ID"] = index
      self.templates.append(camera_config_file)
