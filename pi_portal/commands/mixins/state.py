"""CommandBase mixin to provide configured running state."""

import logging

from pi_portal import config
from pi_portal.modules.configuration import state


class CommandManagedStateMixin:
  """Provide configured state to a CLI command."""

  def load_state(
      self,
      debug: bool,
      file_path: str = config.PATH_USER_CONFIG_INSTALL,
  ) -> None:
    """Load and configure state.

    :param debug: Enable or disable debug logs.
    :param file_path: The path to the file to load.
    """
    running_state = state.State()
    running_state.load(file_path=file_path)
    if debug:
      running_state.log_level = logging.DEBUG
