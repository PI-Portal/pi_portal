"""Motion integration module."""

import glob
import logging
import os
from typing import List

from pi_portal import config
from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.network import http


class MotionException(Exception):
  """Exceptions for the Motion integration."""


class MotionClient:
  """Integration with the Motion application."""

  snapshot_url = 'http://localhost:8080/{0}/action/snapshot'
  snapshot_file_name = os.path.join(config.PATH_MOTION_CONTENT, 'lastsnap.jpg')
  video_glob_pattern = os.path.join(config.PATH_MOTION_CONTENT, '/*.mp4')

  def __init__(self, log: logging.Logger) -> None:
    user_config = state.State().user_config
    self.http_client = http.HttpClient(log)
    self.http_client.set_basic_auth(
        user_config["MOTION"]["AUTHENTICATION"]["USERNAME"],
        user_config["MOTION"]["AUTHENTICATION"]["PASSWORD"],
    )

  def cleanup_snapshot(self, file_name: str) -> None:
    """Delete snapshot locally.

    :param file_name: The path to the file to delete.
    :raises: :class:`MotionException`
    """
    try:
      os.remove(file_name)
    except OSError as exc:
      raise MotionException("Unable to remove snapshot.") from exc

  def get_latest_video_filename(self) -> str:
    """Retrieve the filename of the latest video recording.

    :returns: The path of the latest video file that was created.
    :raises: :class:`MotionException`
    """
    return max(self._list_videos(), key=os.path.getctime)

  def _list_videos(self) -> List[str]:
    return glob.glob(self.video_glob_pattern)

  def take_snapshot(self, camera: int = 0) -> None:
    """Take a snapshot with Motion.

    :param camera: The camera index to use.
    :raises: :class:`MotionException`
    """

    try:
      self.http_client.get(self.snapshot_url.format(camera))
    except http.HttpClientError as exc:
      raise MotionException("Unable to take snapshot.") from exc
