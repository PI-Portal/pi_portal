"""RenderLogIoTemplates class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    FileSystemTemplate,
    RenderTemplatesAction,
)


class RenderLogIoTemplates(RenderTemplatesAction):
  """Render the required log.io integration templates."""

  templates = [
      FileSystemTemplate(
          source='logzio/filebeat.yml',
          destination=config.PATH_FILEBEAT_CONFIG,
          permissions="600",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      ),
  ]
