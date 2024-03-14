"""ActionBase class."""

import abc
import logging


class ActionBase(abc.ABC):
  """Generic installer action component.

  :param log: The logging instance for this action.
  """

  log: logging.Logger

  def __init__(
      self,
      log: logging.Logger,
  ):
    self.log = log

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke this action."""
