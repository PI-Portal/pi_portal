"""StepConfigureMotion class."""

from ..bases import base_step
from . import (
    action_create_paths,
    action_motion_service_disable,
    action_motion_service_stop,
    action_render_templates,
)


class StepConfigureMotion(base_step.StepBase):
  """Configure the motion service."""

  actions = [
      action_motion_service_stop.StopMotionServiceAction,
      action_motion_service_disable.DisableMotionServiceAction,
      action_create_paths.CreateMotionPathsAction,
      action_render_templates.RenderMotionTemplatesAction,
  ]
  logging_begin_message = "Configuring the motion service..."
  logging_end_message = "Done configuring the motion service"
