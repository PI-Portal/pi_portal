"""Camera client base class."""

import abc
import logging

from pi_portal.modules.configuration import state


class CameraException(Exception):
  """Exceptions for the camera integration."""


class CameraClientBase(abc.ABC):
  """Camera client base class.

  :param log: The logger instance to use.
  """

  def __init__(self, log: logging.Logger) -> None:
    self.log = log
    self.current_state = state.State()

  @abc.abstractmethod
  def take_snapshot(self, camera: int) -> None:
    """Take a snapshot with the specified camera.

    :param camera: The camera index to use.
    :raises: :class:`CameraException`
    """
