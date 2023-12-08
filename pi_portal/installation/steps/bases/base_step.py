"""StepBase class."""

import abc
import logging


class StepBase(abc.ABC):
  """Generic installer step."""

  log: logging.Logger

  def __init__(
      self,
      log: logging.Logger,
  ):
    self.log = log

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke this step."""
