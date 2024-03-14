"""StepCreateLoggingPaths class."""

from ..bases import base_step
from . import action_create_paths


class StepCreateLoggingPaths(base_step.StepBase):
  """Create pi_portal logging paths."""

  actions = [action_create_paths.CreateLoggingPathsAction]
  logging_begin_message = "Initializing logging paths ..."
  logging_end_message = "Done initializing logging paths."
