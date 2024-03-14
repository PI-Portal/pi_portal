"""StepConfigureSupervisord class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    RenderTemplatesAction,
)
from pi_portal.installation.templates.config_file import ConfileFileTemplate


class RenderSupervisordTemplatesAction(RenderTemplatesAction):
  """Render the required supervisord templates."""

  templates = [
      ConfileFileTemplate(
          source='supervisor/supervisord.conf',
          destination=config.PATH_SUPERVISOR_CONFIG,
          permissions="600",
          user="root",
      ),
  ]
