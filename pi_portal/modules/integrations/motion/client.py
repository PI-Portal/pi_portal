"""Motion integration module."""

import glob
import logging
import os
from typing import List

from pi_portal import config
from pi_portal.modules.integrations.network import http
from pi_portal.modules.integrations.s3 import client as s3_client


class MotionException(Exception):
  """Exceptions for the Motion integration."""


class MotionClient:
  """Integration with the Motion application."""

  snapshot_url = 'http://localhost:8080/0/action/snapshot'
  snapshot_file_name = os.path.join(config.PATH_MOTION_CONTENT, 'lastsnap.jpg')
  video_glob_pattern = os.path.join(config.PATH_MOTION_CONTENT, '/*.mp4')

  def __init__(self, log: logging.Logger) -> None:
    self.s3_client = s3_client.S3BucketClient()
    self.http_client = http.HttpClient(log)

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

  def take_snapshot(self) -> None:
    """Take a snapshot with Motion.

    :raises: :class:`MotionException`
    """

    try:
      self.http_client.get(self.snapshot_url)
    except http.HttpClientError as exc:
      raise MotionException("Unable to take snapshot.") from exc
