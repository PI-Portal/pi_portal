"""Borg monostate of task scheduler's flags."""
from typing import Any, Dict


class FlagState:
  """Monostate of the task scheduler's flags."""

  __shared_state: Dict[str, Any] = {}

  def __init__(self) -> None:
    self.__dict__ = self.__shared_state
    if not self.__shared_state:
      self.flags = Flags()


class Flags:
  """Individual flag values."""

  FLAG_CAMERA_DISABLED_BY_CRON: bool = False
