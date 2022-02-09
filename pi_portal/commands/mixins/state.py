"""CommandBase mixin to provide configured running state."""

import logging

from pi_portal.modules.configuration import state


class CommandManagedStateMixin:
  """Provide configured state to a CLI command."""

  def load_state(self, debug: bool) -> None:
    """Load and configure state.

    :param debug: Enable or disable debug logs.
    """
    running_state = state.State()
    running_state.load()
    if debug:
      running_state.log_level = logging.DEBUG
