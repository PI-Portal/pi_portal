"""StepConfigureLogzIo class."""

from ..bases import base_step
from . import action_create_paths, action_remote_files, action_render_templates


class StepConfigureLogzIo(base_step.StepBase):
  """Configure the logz.io integration."""

  actions = [
      action_create_paths.CreateLogzIoPathsAction,
      action_remote_files.RemoteFileLogzIoAction,
      action_render_templates.RenderLogIoTemplates,
  ]
  logging_begin_message = "Configuring the logz.io integration ..."
  logging_end_message = "Done configuring the logz.io integration."
