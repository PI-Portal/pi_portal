"""CLI command to load the running config for Pi Portal."""

import logging

from pi_portal.modules.configuration import state
from .bases import toggle_command


class LoadStateCommand(toggle_command.ToggleCommandBase):
  """CLI command to load the running config for Pi Portal."""

  def invoke(self) -> None:
    """Invoke the command."""

    running_state = state.State()
    running_state.load()
    if self.toggle:
      running_state.log_level = logging.DEBUG
