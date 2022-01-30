"""Motion integration module."""

import glob
import os

import requests
from pi_portal import config
from pi_portal.modules.integrations import s3
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class MotionException(BaseException):
  """Exceptions for the Motion integration."""


class Motion:
  """Integration with the Motion application."""

  snapshot_url = 'http://localhost:8080/0/action/snapshot'
  snapshot_fname = os.path.join(config.MOTION_FOLDER, 'lastsnap.jpg')
  snapshot_retries = 10
  s3_retries = 3

  def __init__(self):
    self.data_folder = config.MOTION_FOLDER
    self.s3_client = s3.S3Bucket()

  def archive_video(self, file_name: str):
    """Copy video to S3 for retention and delete locally.

    :param file_name: The path to upload and then remove.
    """
    try:
      self.s3_client.upload(file_name)
      os.remove(file_name)
    except (s3.S3BucketException, OSError) as exc:
      raise MotionException("Unable to archive video to S3.") from exc

  def cleanup_snapshot(self, file_name: str):
    """Delete snapshot locally.

    :param file_name: The path to remove.
    """
    try:
      os.remove(file_name)
    except OSError as exc:
      raise MotionException("Unable to remove snapshot.") from exc

  def get_latest_video_filename(self) -> str:
    """Retrieve the filename of the latest video recording.

    :return: The path of the latest video file that was created.
    """
    return max(self._list_videos(), key=os.path.getctime)

  def _list_videos(self):
    return glob.glob(os.path.join(self.data_folder, '/*.mp4'))

  def take_snapshot(self):
    """Take a snapshot with Motion."""

    retry_strategy = Retry(total=self.snapshot_retries)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    response = http.get(self.snapshot_url)
    if response.status_code != requests.status_codes.codes.ok:
      raise MotionException("Unable to take snapshot.")
