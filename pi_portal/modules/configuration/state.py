"""Borg monostate of the current running configuration."""

import logging
import uuid
from typing import Any, Dict, cast

from pi_portal.modules.configuration.user_config import (
    TypeUserConfig,
    UserConfiguration,
)


class State:
  """Monostate of the current running configuration."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self) -> None:
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.user_config: TypeUserConfig = cast(TypeUserConfig, {})
      self.log_uuid = str(uuid.uuid4())
      self._log_level = logging.INFO

  @property
  def log_level(self) -> int:
    """Return the currently configured logging level.

    :returns: The currently configured logging level.
    """

    return self._log_level

  @log_level.setter
  def log_level(self, level: int) -> None:
    """Configure the logging level.

    :param level: The desired logging level.
    """

    self._log_level = level

  def load(self, file_path: str = "config.json") -> None:
    """Load the end user configuration.

    :param file_path: The path to the file to load.
    """

    configuration = UserConfiguration()
    configuration.load(file_path=file_path)
    self.user_config = configuration.user_config
