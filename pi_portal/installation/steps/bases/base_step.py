"""StepBase class."""

import logging
from typing import List, Type

from pi_portal.installation.actions.bases import base_action


class StepBase:
  """Generic installer step.

  :param log: The logging instance for this step.
  """

  actions: List[Type[base_action.ActionBase]]
  log: logging.Logger
  logging_begin_message: str
  logging_end_message: str

  def __init__(
      self,
      log: logging.Logger,
  ):
    self.log = log

  def invoke(self) -> None:
    """Invoke this step."""

    self.log.info(self.logging_begin_message)

    for action_class in self.actions:
      action = action_class(self.log)
      action.invoke()

    self.log.info(self.logging_end_message)
