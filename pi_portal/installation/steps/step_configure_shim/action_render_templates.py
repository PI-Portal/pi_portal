"""RenderPiPortalShimTemplatesAction class."""

from pi_portal import config
from pi_portal.installation.actions.action_render_templates import (
    FileSystemTemplate,
    RenderTemplatesAction,
)


class RenderPiPortalShimTemplatesAction(RenderTemplatesAction):
  """Render the required pi_portal shim templates."""

  templates = [
      FileSystemTemplate(
          source='shim/portal',
          destination=config.PI_PORTAL_SHIM,
          permissions="755",
          user=config.PI_PORTAL_USER,
          group=config.PI_PORTAL_USER,
      )
  ]
