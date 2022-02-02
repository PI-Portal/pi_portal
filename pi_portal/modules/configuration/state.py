"""Borg monostate of the current running configuration."""

from typing import Any, Dict

from pi_portal.modules.configuration.user_config import UserConfiguration


class State:
  """Monostate of the current running configuration."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self) -> None:
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.user_config: Dict[str, str] = {}

  def load(self) -> None:
    """Load the end user configuration."""

    configuration = UserConfiguration()
    configuration.load()
    self.user_config = configuration.user_config
