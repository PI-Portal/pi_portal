"""A camera client for camera task processors."""
import logging
from typing import Any

from pi_portal.modules.integrations.camera.service_client import CameraClient


class CameraClientMixin:
  """A camera client for camera task processors.

  :param log: The logging instance to use.
  """

  log: logging.Logger

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)
    self.client = CameraClient(self.log)
