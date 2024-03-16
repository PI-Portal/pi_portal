"""StepConfigureSupervisord class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    FileSystemTemplate,
    RenderTemplatesAction,
)


class RenderSupervisordTemplatesAction(RenderTemplatesAction):
  """Render the required supervisord templates."""

  templates = [
      FileSystemTemplate(
          source='supervisor/supervisord.conf',
          destination=config.PATH_SUPERVISOR_CONFIG,
          permissions="600",
          user="root",
          group="root",
      ),
  ]
