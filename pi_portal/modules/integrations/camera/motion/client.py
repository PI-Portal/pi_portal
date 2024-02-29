"""Camera client for the Motion application."""

import logging

from pi_portal.modules.integrations.camera.bases.client import (
    CameraClientBase,
    CameraException,
)
from pi_portal.modules.integrations.network import http


class MotionClient(CameraClientBase):
  """Camera client for the Motion application.

  :param log: The logger instance to use.
  """

  snapshot_url = 'http://localhost:8080/{0}/action/snapshot'

  def __init__(self, log: logging.Logger) -> None:
    super().__init__(log)
    motion_config = self.current_state.user_config["CAMERA"]["MOTION"]
    self.http_client = http.HttpClient(self.log)
    self.http_client.set_basic_auth(
        motion_config["AUTHENTICATION"]["USERNAME"],
        motion_config["AUTHENTICATION"]["PASSWORD"],
    )

  def take_snapshot(self, camera: int) -> None:
    """Take a snapshot with Motion.

    :param camera: The camera index to use.
    :raises: :class:`CameraException`
    """

    try:
      self.http_client.get(self.snapshot_url.format(camera))
    except http.HttpClientError as exc:
      raise CameraException("Unable to take snapshot.") from exc
