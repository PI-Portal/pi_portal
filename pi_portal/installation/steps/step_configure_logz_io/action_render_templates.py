"""RenderLogIoTemplates class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    RenderTemplatesAction,
)
from pi_portal.installation.templates.config_file import ConfileFileTemplate


class RenderLogIoTemplates(RenderTemplatesAction):
  """Render the required log.io integration templates."""

  templates = [
      ConfileFileTemplate(
          source='logzio/filebeat.yml',
          destination=config.PATH_FILEBEAT_CONFIG,
          permissions="600",
          user=config.PI_PORTAL_USER,
      ),
  ]
