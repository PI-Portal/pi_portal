"""Camera client base class."""

import abc
import logging
import shutil

from pi_portal import config
from pi_portal.modules.configuration import state


class CameraException(Exception):
  """Exceptions for the camera integration."""


class CameraClientBase(abc.ABC):
  """Camera client base class.

  :param log: The logger instance to use.
  """

  def __init__(self, log: logging.Logger) -> None:
    self.log = log
    self.camera_config = state.State().user_config["CAMERA"]

  def is_disk_space_available(self) -> bool:
    """Check the camera path disk utilization against the threshold.

    :returns: A boolean indicating if there is enough disk space for the camera.
    """

    threshold_path = config.PATH_CAMERA_CONTENT
    threshold_value = self.camera_config["DISK_SPACE_MONITOR"]["THRESHOLD"]
    free_space = shutil.disk_usage(threshold_path).free

    return free_space >= threshold_value * 1000000

  @abc.abstractmethod
  def take_snapshot(self, camera: int) -> None:
    """Take a snapshot with the specified camera.

    :param camera: The camera index to use.
    :raises: :class:`CameraException`
    """
