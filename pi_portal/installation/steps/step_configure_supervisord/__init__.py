"""StepConfigureSupervisord class."""

from ..bases import base_step
from . import action_create_paths, action_render_templates


class StepConfigureSupervisord(base_step.StepBase):
  """Configure the supervisord service."""

  actions = [
      action_create_paths.CreateSupervisordPathsAction,
      action_render_templates.RenderSupervisordTemplatesAction,
  ]
  logging_begin_message = "Configuring the supervisord service ..."
  logging_end_message = "Done configuring the supervisord service."
