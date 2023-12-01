"""Test Motion Integration."""

import os
from typing import cast
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations import motion
from pi_portal.modules.integrations.s3 import client


class TestMotion(TestCase):
  """Test the Motion class."""

  @mock_state.patch
  def setUp(self) -> None:
    self.motion_client = motion.Motion()
    self.motion_client.s3_client = mock.MagicMock()

  def _mock_s3_client(self) -> mock.Mock:
    return cast(mock.Mock, self.motion_client.s3_client)

  @mock_state.patch
  def test_initialization(self) -> None:
    motion_client = motion.Motion()
    self.assertEqual(
        self.motion_client.snapshot_url,
        'http://localhost:8080/0/action/snapshot'
    )
    self.assertEqual(
        motion_client.snapshot_fname, '/var/lib/motion/lastsnap.jpg'
    )
    self.assertEqual(motion_client.snapshot_retries, 10)
    self.assertEqual(motion_client.s3_retries, 3)
    self.assertEqual(
        motion_client.video_glob_pattern,
        os.path.join(config.MOTION_FOLDER, '/*.mp4')
    )
    self.assertIsInstance(motion_client.s3_client, client.S3BucketClient)

  @mock.patch(motion.__name__ + ".requests.Session.get")
  def test_take_snapshot_failure(self, m_get: mock.Mock) -> None:
    m_get.session.stream.side_effect = motion.requests.ConnectionError
    with self.assertRaises(motion.MotionException):
      self.motion_client.take_snapshot()

  @mock.patch(motion.__name__ + ".requests.Session.get")
  def test_take_snapshot_success(self, m_get: mock.Mock) -> None:
    m_get.return_value.status_code = motion.requests.status_codes.codes.ok
    self.motion_client.take_snapshot()

  @mock.patch(motion.__name__ + ".glob.glob")
  @mock.patch(motion.__name__ + ".os.path.getctime")
  def test_get_latest_video_filename(
      self, m_ctime: mock.Mock, m_glob: mock.Mock
  ) -> None:
    m_glob.return_value = ["1.mp4", "2.mp4"]
    m_ctime.side_effect = [1.01, 1.02]
    fname = self.motion_client.get_latest_video_filename()
    self.assertEqual(fname, m_glob.return_value[1])

  @mock.patch(motion.__name__ + ".os.remove")
  def test_archive_video(self, m_remove: mock.Mock) -> None:
    mock_video_name = "mock_video.mp4"
    self.motion_client.archive_video(mock_video_name)
    self._mock_s3_client().upload.assert_called_once_with(mock_video_name)
    m_remove.assert_called_once_with(mock_video_name)

  @mock.patch(motion.__name__ + ".os.remove")
  def test_archive_video_exception(self, m_remove: mock.Mock) -> None:
    mock_video_name = "mock_video.mp4"
    self._mock_s3_client(
    ).upload.side_effect = client.S3BucketException("Boom!")

    with self.assertRaises(motion.MotionException):
      self.motion_client.archive_video(mock_video_name)

    self._mock_s3_client().upload.assert_called_once_with(mock_video_name)
    m_remove.assert_not_called()

  @mock.patch(motion.__name__ + ".os.remove")
  def test_cleanup_snapshot(self, m_remove: mock.Mock) -> None:
    mock_snapshot_name = "mock_snapshot.jpg"
    self.motion_client.cleanup_snapshot(mock_snapshot_name)
    m_remove.assert_called_once_with(mock_snapshot_name)

  @mock.patch(motion.__name__ + ".os.remove")
  def test_cleanup_snapshot_exception(self, m_remove: mock.Mock) -> None:
    mock_snapshot_name = "mock_snapshot.jpg"
    m_remove.side_effect = OSError("Boom!")

    with self.assertRaises(motion.MotionException):
      self.motion_client.cleanup_snapshot(mock_snapshot_name)

    m_remove.assert_called_once_with(mock_snapshot_name)
