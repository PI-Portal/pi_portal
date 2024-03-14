"""StepCreateDataPaths class."""

from ..bases import base_step
from . import action_create_paths


class StepCreateDataPaths(base_step.StepBase):
  """Initialize the required data storage paths."""

  actions = [action_create_paths.CreateDataPathsAction]
  logging_begin_message = "Initializing data paths ..."
  logging_end_message = "Done initializing data paths."
