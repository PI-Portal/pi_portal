"""Motion integration module."""

import logging

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.network import http


class MotionException(Exception):
  """Exceptions for the Motion integration."""


class MotionClient:
  """Integration with the Motion application."""

  snapshot_url = 'http://localhost:8080/{0}/action/snapshot'

  def __init__(self, log: logging.Logger) -> None:
    user_config = state.State().user_config
    self.http_client = http.HttpClient(log)
    self.http_client.set_basic_auth(
        user_config["MOTION"]["AUTHENTICATION"]["USERNAME"],
        user_config["MOTION"]["AUTHENTICATION"]["PASSWORD"],
    )

  def take_snapshot(self, camera: int = 0) -> None:
    """Take a snapshot with Motion.

    :param camera: The camera index to use.
    :raises: :class:`MotionException`
    """

    try:
      self.http_client.get(self.snapshot_url.format(camera))
    except http.HttpClientError as exc:
      raise MotionException("Unable to take snapshot.") from exc
