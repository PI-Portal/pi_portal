"""Borg monostate of the current running configuration."""

from typing import Any, Dict

from pi_portal.modules.configuration import config_file


class State:
  """Borg monostate of the current running configuration."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self):
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.user_config = {}

  def load(self):
    """Load the user configuration file into the monostate."""

    configuration = config_file.UserConfiguration()
    self.user_config = configuration.load()
