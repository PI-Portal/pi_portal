"""StepConfigurePiPortalShim class."""

from ..bases import base_step
from . import action_render_templates


class StepConfigurePiPortalShim(base_step.StepBase):
  """Configure the pi_portal shim script."""

  actions = [
      action_render_templates.RenderPiPortalShimTemplatesAction,
  ]
  logging_begin_message = "Configuring the pi_portal shim script ..."
  logging_end_message = "Done configuring the pi_portal shim script."
