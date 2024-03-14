"""StepEnsureRoot class."""

from ..bases import base_step
from . import action_ensure_root


class StepEnsureRoot(base_step.StepBase):
  """Ensure that the installer is running as root."""

  actions = [action_ensure_root.EnsureRootAction]
  logging_begin_message = "Ensuring that the installer is running as root ..."
  logging_end_message = "Done ensuring that the installer is running as root."
