"""Test Motion Integration."""

import os
from unittest import TestCase, mock

from pi_portal import config
from pi_portal.modules import motion, s3
from pi_portal.modules.tests.fixtures import environment


class TestMotion(TestCase):
  """Test the Motion class."""

  @environment.patch
  def setUp(self):
    self.motion_client = motion.Motion()
    self.motion_client.s3_client = mock.MagicMock()

  @environment.patch
  def test_initialization(self):
    motion_client = motion.Motion()
    self.assertEqual(
        self.motion_client.snapshot_url,
        'http://localhost:8080/0/action/snapshot'
    )
    self.assertEqual(motion_client.snapshot_fname, 'lastsnap.jpg')
    self.assertEqual(motion_client.snapshot_retries, 10)
    self.assertEqual(motion_client.s3_retries, 3)
    self.assertEqual(motion_client.data_folder, config.MOTION_FOLDER)
    self.assertIsInstance(motion_client.s3_client, s3.S3Bucket)

  @mock.patch(motion.__name__ + ".requests.Session.get")
  def test_take_snapshot_failure(self, m_get):
    m_get.session.stream.side_effect = motion.requests.ConnectionError
    with self.assertRaises(motion.MotionException):
      self.motion_client.take_snapshot()

  @mock.patch(motion.__name__ + ".requests.Session.get")
  def test_take_snapshot_success(self, m_get):
    m_get.return_value.status_code = motion.requests.status_codes.codes.ok
    self.motion_client.take_snapshot()

  @mock.patch(motion.__name__ + ".glob.glob")
  @mock.patch(motion.__name__ + ".os.path.getctime")
  def test_get_latest_video_filename(self, m_ctime, m_glob):
    m_glob.return_value = ["1.mp4", "2.mp4"]
    m_ctime.side_effect = [1.01, 1.02]
    fname = self.motion_client.get_latest_video_filename()
    self.assertEqual(fname, m_glob.return_value[1])

  @mock.patch(motion.__name__ + ".glob.glob")
  @mock.patch(motion.__name__ + ".os.remove")
  def test_cleanup_videos(self, m_remove, m_glob):
    m_glob.return_value = ["1.mp4", "2.mp4"]
    self.motion_client.cleanup_videos()

    m_glob.assert_called_once_with(
        os.path.join(self.motion_client.data_folder, '/*.mp4')
    )
    for fname in m_glob.return_value:
      m_remove.assert_any_call(fname)
    self.assertEqual(m_remove.call_count, len(m_glob.return_value))

  @mock.patch(motion.__name__ + ".glob.glob")
  @mock.patch(motion.__name__ + ".os.remove")
  def test_cleanup_snapshots(self, m_remove, m_glob):
    m_glob.return_value = ["1.mp4", "2.mp4", self.motion_client.snapshot_fname]
    self.motion_client.cleanup_snapshots()

    m_glob.assert_called_once_with(
        os.path.join(self.motion_client.data_folder, '/*.mp4')
    )
    for fname in m_glob.return_value:
      if fname != self.motion_client.snapshot_fname:
        m_remove.assert_any_call(fname)
    self.assertEqual(m_remove.call_count, len(m_glob.return_value))

  @mock.patch(motion.__name__ + ".os.remove")
  def test_archive_video_to_s3(self, m_remove):
    mock_video_name = "mock_video.mp4"
    self.motion_client.archive_video_to_s3(mock_video_name)
    self.motion_client.s3_client.upload.assert_called_once_with(mock_video_name)
    m_remove.assert_called_once_with(mock_video_name)

  @mock.patch(motion.__name__ + ".os.remove")
  def test_archive_video_to_s3_failure(self, m_remove):
    mock_video_name = "mock_video.mp4"
    self.motion_client.s3_client.upload.side_effect = s3.S3BucketException(
        "Boom!"
    )

    with self.assertRaises(motion.MotionException):
      self.motion_client.archive_video_to_s3(mock_video_name)

    self.motion_client.s3_client.upload.assert_called_once_with(mock_video_name)
    m_remove.assert_not_called()
